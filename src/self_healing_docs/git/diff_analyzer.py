import subprocess
from pathlib import Path

def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()

def changed_python_paths(repo: Path, base: str, head: str) -> list[str]:
    out = git(repo, "diff", "--name-only", "--diff-filter=ACMR", f"{base}...{head}", "--", "*.py")
    return sorted(set(x for x in out.splitlines() if x))

def file_at_ref(repo: Path, ref: str, path: str):
    p = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{path}"], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None
