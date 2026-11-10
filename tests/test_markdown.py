from self_healing_docs.parsers.markdown_parser import parse_markdown

def test_heading_in_code_fence_is_ignored(tmp_path):
    p = tmp_path / "README.md"
    p.write_text("# API\ntext\n```md\n## fake\n```\n## Other\nmore\n")
    assert [x.heading for x in parse_markdown(p, "README.md")] == ["API", "Other"]
