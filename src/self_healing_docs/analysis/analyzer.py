import re
from pathlib import Path
from self_healing_docs.git.diff_analyzer import changed_python_paths, file_at_ref
from self_healing_docs.parsers.python_parser import classify
from self_healing_docs.parsers.markdown_parser import markdown_files, parse_markdown
from self_healing_docs.models import SymbolChange, Finding

def analyze(repo: Path, base: str, head: str, docs: list[str]):
    changes = []
    for source_path in changed_python_paths(repo, base, head):
        try: classified = classify(file_at_ref(repo, base, source_path), file_at_ref(repo, head, source_path))
        except SyntaxError: continue
        for name, kind, before, after in classified:
            changes.append(SymbolChange(name, source_path, kind, before[1] if before else None,
                after[1] if after else None, before[2] if before else None, after[2] if after else None))
    findings = []
    for path in markdown_files(repo, docs):
        rel = path.relative_to(repo).as_posix()
        for section in parse_markdown(path, rel):
            for change in changes:
                if re.search(rf"(?<![\\w]){re.escape(change.name)}(?![\\w])", section.text):
                    findings.append(Finding(change.name, change.source_file, rel, section.heading,
                        section.start_line, change.change_type,
                        "Changed Python symbol is mentioned in this section; verify its claims."))
    return changes, sorted(findings, key=lambda x: (x.documentation_file, x.section_start_line, x.symbol))
