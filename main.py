import hashlib
from pathlib import Path

TEXT = "fix: cured the stale cache by caching everything forever \u2014 welcome back to last Tuesday, daily"

def main() -> None:
    out = Path("/output/entry.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    data = TEXT.encode("utf-8")
    out.write_bytes(data)
    back = out.read_bytes()
    if hashlib.sha256(back).hexdigest() != hashlib.sha256(data).hexdigest():
        raise SystemExit("digest mismatch on read-back")

if __name__ == "__main__":
    main()
