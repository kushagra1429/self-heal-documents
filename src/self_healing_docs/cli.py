import argparse, json, os, sys
from pathlib import Path
from self_healing_docs.analysis.analyzer import analyze

def main():
    p = argparse.ArgumentParser(description="Find Markdown sections potentially affected by Python changes")
    p.add_argument("--repo", default="."); p.add_argument("--base", required=True); p.add_argument("--head", default="HEAD")
    p.add_argument("--docs", nargs="+", default=["README.md", "docs"]); p.add_argument("--output")
    a = p.parse_args()
    try:
        repo = Path(a.repo).resolve(); docs = [part for item in a.docs for part in item.split()]\n        changes, findings = analyze(repo, a.base, a.head, docs)
        report = {"schema_version":"1.0", "base":a.base, "head":a.head,
                  "changes":[vars(x) for x in changes], "findings":[x.to_dict() for x in findings]}
        rendered = json.dumps(report, indent=2) + "\\n"
        if a.output:
            out = Path(a.output); out = out if out.is_absolute() else repo / out
            out.parent.mkdir(parents=True, exist_ok=True); out.write_text(rendered, encoding="utf-8")
        else: print(rendered, end="")
        summary = os.getenv("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as f:
                f.write("## Self-Healing Documentation Review\\n\\n")
                f.write(f"Found **{len(findings)} candidate(s)** for human review.\\n")
                for x in findings: f.write(f"- `{x.documentation_file}:{x.section_start_line}` — `{x.symbol}` ({x.change_type})\\n")
        return 0
    except Exception as e:
        print(f"self-healing-docs: {e}", file=sys.stderr); return 2
if __name__ == "__main__": raise SystemExit(main())
