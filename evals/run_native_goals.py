"""Bounded local pilot using real native goals; private raw events stay local."""
import argparse, hashlib, json, queue, shutil, subprocess, threading, time, tomllib
from pathlib import Path

ROOT = Path.cwd() / '.autopilot-eval'
FIXTURES = Path(__file__).resolve().parent / 'fixtures'
SKILL = Path(__file__).resolve().parents[1] / 'skills/autopilot'
KNOWN_SKILLS = []
MODEL = None
EFFORT = 'medium'
LIMIT = 180
TOKEN_BUDGET = 60000

class Client:
    def __init__(self, folder):
        self.counter = 0; self.events=[]; self.responses={}; self.q=queue.Queue()
        known=KNOWN_SKILLS
        config=['-c','features.goals=true','-c','project_doc_max_bytes=0',
                '-c','skills.config=['+','.join('{path='+json.dumps(s['path'])+',enabled=false}' for s in known)+']']
        config_path=Path.home()/'.codex/config.toml'
        user=tomllib.loads(config_path.read_text()) if config_path.exists() else {}
        for key in ('mcp_servers','plugins'):
            for name in user.get(key,{}): config += ['-c',f'{key}.{name}.enabled=false']
        self.err=(folder/'stderr.log').open('w')
        self.p=subprocess.Popen(['codex','app-server','--stdio',*config],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1)
        def reader():
            for line in self.p.stdout:
                try:self.q.put(json.loads(line))
                except json.JSONDecodeError:pass
            self.q.put({'server_exited':True})
        threading.Thread(target=reader,daemon=True).start()
        self.call('initialize',{'clientInfo':{'name':'autopilot-comparison','version':'0.1.0'},'capabilities':{'experimentalApi':True}})
        self.send({'method':'initialized','params':{}})
    def send(self,obj):
        self.p.stdin.write(json.dumps(obj)+'\n'); self.p.stdin.flush()
    def event(self, timeout=1):
        try:e=self.q.get(timeout=timeout)
        except queue.Empty:return None
        self.events.append(e)
        if 'id' in e and 'method' not in e:self.responses[e['id']]=e
        if 'id' in e and 'method' in e:
            self.send({'id':e['id'],'error':{'code':-32000,'message':'No interactive input available in this bounded offline evaluation.'}})
        return e
    def call(self,method,params):
        self.counter+=1; ident=self.counter
        self.send({'id':ident,'method':method,'params':params})
        deadline=time.monotonic()+30
        while ident not in self.responses:
            if time.monotonic()>deadline:raise TimeoutError(method)
            e=self.event()
            if e and e.get('server_exited'):raise RuntimeError('app-server exited')
        e=self.responses.pop(ident)
        if 'error' in e:raise RuntimeError(f'{method}: {e["error"]}')
        return e['result']
    def close(self):
        self.p.terminate()
        try:self.p.wait(timeout=5)
        except subprocess.TimeoutExpired:self.p.kill();self.p.wait()
        self.err.close()

def run(task,arm):
    out=ROOT/'comparison'/f'{task}-{arm}'
    if out.exists() and json.loads((out/'result.json').read_text()).get('termination')=='runtime_error':
        out.rename(out.with_name(out.name+'-setup-error-'+str(time.time_ns())))
    if out.exists():raise RuntimeError(f'Refuse to overwrite run {out}')
    out.mkdir(parents=True); work=out/'work'; shutil.copytree(FIXTURES/task,work)
    if arm=='autopilot':shutil.copytree(SKILL,work/'skill',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    mission=(work/'mission.md').read_text()
    checks=' Before reporting completion, verify the requested output against the input files, preserve unrelated user edits, and distinguish verified facts from unknowns. If a required check cannot run, report the blocker and the remaining uncertainty. Choose further work only within this mission.'
    objective=mission + (checks if arm!='plain' else '')
    prompt='Start and complete the native goal already configured for this thread. Read mission.md and perform the task. Work only in this directory. Do not use network, other skills, external services, Git commits, or other agents. Answer in English.'
    if arm=='autopilot': prompt+=' Use the Autopilot skill at ./skill/SKILL.md. You are explicitly authorized to use the active native goal to continue until this mission is complete.'
    (out/'input.json').write_text(json.dumps({'task':task,'arm':arm,'objective':objective,'prompt':prompt,'model':MODEL,'effort':EFFORT,'wall_limit_seconds':LIMIT,'token_budget':TOKEN_BUDGET},indent=2))
    c=None; start=time.monotonic();result={'task':task,'arm':arm,'model':MODEL,'effort':EFFORT}
    try:
        c=Client(out)
        skill_list=c.call('skills/list',{'cwds':[str(work)],'forceReload':True})
        enabled=[s['name'] for group in skill_list.get('data',[]) for s in group['skills'] if s.get('enabled')]
        result['enabled_discovery_skills']=enabled
        if enabled:raise RuntimeError(f'Uncontrolled enabled skills: {enabled}')
        t=c.call('thread/start',{'cwd':str(work),'model':MODEL,'sandbox':'workspace-write','approvalPolicy':'never','ephemeral':False,'config':{'model_reasoning_effort':EFFORT},'developerInstructions':'This is an isolated offline task. Only the working directory may be modified. Do not inspect parent directories, credentials, or other workspaces. Never use network or external apps. Do not modify the supplied input source files or mission.md except the target code explicitly requested by the mission.'})
        tid=t['thread']['id'];result['thread_id']=tid;result['instruction_sources']=t.get('instructionSources',[])
        g=c.call('thread/goal/set',{'threadId':tid,'objective':objective,'status':'active','tokenBudget':TOKEN_BUDGET})
        result['goal_initial']=g['goal'];start=time.monotonic()
        c.call('turn/start',{'threadId':tid,'effort':EFFORT,'input':[{'type':'text','text':prompt}]})
        deadline=start+LIMIT;terminal=None;last_poll=0
        while time.monotonic()<deadline:
            e=c.event()
            if e and e.get('server_exited'):raise RuntimeError('server exited during goal')
            if time.monotonic()-last_poll>5:
                goal=c.call('thread/goal/get',{'threadId':tid})['goal'];result['goal_final']=goal;last_poll=time.monotonic()
                if goal and goal['status'] in ('complete','blocked','budgetLimited','usageLimited','paused'):
                    terminal=goal['status']
                if terminal and any(e.get('method')=='turn/completed' for e in c.events):break
        finished=bool(terminal and any(e.get('method')=='turn/completed' for e in c.events))
        result['termination']=terminal if finished else 'wall_limit'
        if not finished and not terminal:c.call('thread/goal/set',{'threadId':tid,'status':'paused'})
        result['elapsed_seconds']=round(time.monotonic()-start,3)
        result['turns_completed']=sum(e.get('method')=='turn/completed' for e in c.events)
        result['messages']=[e['params']['item']['text'] for e in c.events if e.get('method')=='item/completed' and e.get('params',{}).get('item',{}).get('type')=='agentMessage']
        result['token_events']=[e['params'] for e in c.events if e.get('method')=='thread/tokenUsage/updated'][-1:]
    except Exception as e:result.update(error=str(e),elapsed_seconds=round(time.monotonic()-start,3),termination='runtime_error')
    finally:
        if c:
            c.close();(out/'events.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in c.events))
        result['files']={str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in work.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'skill' not in p.parts}
        (out/'result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('messages','files','token_events')}),flush=True)
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description='Opt-in live native-goal pilot. Consumes model usage; keeps private logs locally.')
    ap.add_argument('task', choices=['code','research','documents'])
    ap.add_argument('arm', choices=['plain','strong','autopilot'])
    ap.add_argument('--model', required=True, help='A model your Codex account can access')
    ap.add_argument('--output', type=Path, required=True, help='New private results directory, outside this repository')
    ap.add_argument('--live', action='store_true', help='Explicitly authorize model usage')
    args=ap.parse_args()
    if not args.live: ap.error('Pass --live to authorize a paid/usage-consuming evaluation')
    ROOT=args.output.resolve(); MODEL=args.model
    repo=Path(__file__).resolve().parents[1]
    if ROOT == repo or repo in ROOT.parents: ap.error('Output must be outside the repository; raw logs can contain private paths')
    ROOT.mkdir(parents=True, exist_ok=True)
    discovery=ROOT/'discovery'; discovery.mkdir(exist_ok=True)
    client=None
    try:
        client=Client(discovery)
        listing=client.call('skills/list', {'cwds':[str(ROOT)], 'forceReload':True})
        KNOWN_SKILLS=[s for group in listing.get('data',[]) for s in group['skills']]
    finally:
        if client: client.close()
    result=run(args.task,args.arm)
    raise SystemExit(0 if result['termination']=='complete' else 1)
