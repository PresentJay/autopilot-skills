"use strict";
document.querySelectorAll("[data-prompt]").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-prompt]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    document.querySelectorAll(".task-prompt").forEach(panel => { panel.hidden = panel.id !== `prompt-${button.dataset.prompt}`; });
  });
});
const copy = document.getElementById("copy-install");
if (copy) copy.addEventListener("click", async () => {
  const status = document.getElementById("copy-status");
  try {
    await navigator.clipboard.writeText(document.getElementById("install-command").textContent);
    status.textContent = copy.dataset.copied;
  } catch {
    status.textContent = copy.dataset.failed;
    const range = document.createRange();
    range.selectNodeContents(document.getElementById("install-command"));
    const selection = window.getSelection();
    selection.removeAllRanges(); selection.addRange(range);
  }
});
