# Vendor comparison — as of 2026-10-21

Scope: supplied local sources only. Source A states a publication date of 2026-10-01; the supplied files do not establish whether it was updated by the comparison date. Source B's specification is unavailable.

| Question | Vendor A | Vendor B |
|---|---|---|
| Latency | Reported median: **200 ms**, measured with **one request at a time on a local network**. [A, line 1](vendor-a.txt#L1) | **Unknown**: the supplied record says HTTP 403 and specification unavailable. [B error, line 1](vendor-b-error.txt#L1) |
| Offline support | **Unknown**: not described in the supplied specification. [A, line 1](vendor-a.txt#L1) | **Unknown**: no specification content is available. [B error, line 1](vendor-b-error.txt#L1) |

The sources do not support a latency ranking or a conclusion about either vendor's offline capability. A's benchmark does not establish latency under other conditions, and a local-network benchmark does not establish offline support. Missing documentation is not evidence that offline support is absent.

Verification: checked against both supplied files. B's error record also says the previous session did not read the specification; it supplies no vendor capability facts. B's publication date and both requested capabilities remain unknown. No network access was attempted.
