import re
from dataclasses import dataclass
from pathlib import Path
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
@dataclass(frozen=True)
class Section:
    path: str
    heading: str
    start_line: int
    text: str

def parse_markdown(path: Path, relative: str):
    lines = path.read_text(encoding="utf-8").splitlines()
    heads, fenced = [], False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            m = HEADING.match(line)
            if m: heads.append((i, len(m.group(1)), m.group(2)))
    result = []
    for idx, (start, level, title) in enumerate(heads):
        end = len(lines)
        for nxt, nxt_level, _ in heads[idx+1:]:
            if nxt_level <= level:
                end = nxt - 1
                break
        result.append(Section(relative, title, start, "\n".join(lines[start-1:end])))
    return result

def markdown_files(repo: Path, paths: list[str]):
    found, excluded = set(), {".git", ".venv", "venv", "node_modules"}
    for item in paths:
        p = (repo / item).resolve()
        try: p.relative_to(repo.resolve())
        except ValueError: continue
        if p.is_file() and p.suffix.lower() == ".md": found.add(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if not excluded.intersection(f.relative_to(repo).parts): found.add(f)
    return sorted(found)
