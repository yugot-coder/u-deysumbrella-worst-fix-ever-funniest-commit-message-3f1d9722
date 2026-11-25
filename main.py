"""Worst Fix Ever — the funniest commit message for a terrible fix.

Writes the commit-message line to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when set), exactly as bytes, no trailing
newline. The line is validated against the gate first, and the written
bytes are read back and verified (byte length + sha256) so a bad write
fails loudly. Standard library only, deterministic.
"""
import hashlib
import os
from pathlib import Path

TEXT = "fix: cured the stale cache by caching everything forever \u2014 welcome back to last Tuesday, daily"

MIN_CHARS = 1
MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Check the line against the competition gate."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS) or not text.strip():
        raise SystemExit("gate failed: length")
    if text != text.strip() or "\n" in text or "\r" in text:
        raise SystemExit("gate failed: must be one line, no edge whitespace")


def verify_written_bytes(written: bytes) -> str:
    """Verify the exact bytes read back from entry.txt; return the digest."""
    intended = TEXT.encode("utf-8")
    if len(written) != len(intended) or written != intended:
        raise SystemExit("content mismatch on read-back")
    digest = hashlib.sha256(written).hexdigest()
    if digest != hashlib.sha256(intended).hexdigest():
        raise SystemExit("digest mismatch on read-back")
    return digest


def main() -> None:
    validate_entry(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out = Path(out_dir) / "entry.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = TEXT.encode("utf-8")
    out.write_bytes(data)
    back = out.read_bytes()
    verify_written_bytes(back)


if __name__ == "__main__":
    main()
