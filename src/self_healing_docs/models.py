from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class SymbolChange:
    name: str
    source_file: str
    change_type: str
    old_signature: str | None
    new_signature: str | None
    old_line: int | None
    new_line: int | None

@dataclass(frozen=True)
class Finding:
    symbol: str
    source_file: str
    documentation_file: str
    section_heading: str
    section_start_line: int
    change_type: str
    reason: str
    status: str = "candidate_for_review"

    def to_dict(self):
        return asdict(self)
