import subprocess
from self_healing_docs.analysis.analyzer import analyze

def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()

def test_end_to_end_candidate(tmp_path):
    git(tmp_path, "init", "-q"); git(tmp_path, "config", "user.name", "Test"); git(tmp_path, "config", "user.email", "t@x")
    (tmp_path/"app.py").write_text('def create_user(role="admin"): return role\n')
    (tmp_path/"README.md").write_text('# Users\n`create_user` defaults to admin.\n')
    git(tmp_path, "add", "."); git(tmp_path, "commit", "-qm", "base"); base = git(tmp_path, "rev-parse", "HEAD")
    (tmp_path/"app.py").write_text('def create_user(role="viewer"): return role\n')
    git(tmp_path, "add", "."); git(tmp_path, "commit", "-qm", "change"); head = git(tmp_path, "rev-parse", "HEAD")
    changes, findings = analyze(tmp_path, base, head, ["README.md"])
    assert changes[0].change_type == "signature_changed"
    assert findings[0].symbol == "create_user"
