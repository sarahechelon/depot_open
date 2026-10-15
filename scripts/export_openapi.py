"""Export the OpenAPI schema so API changes are reviewable in PRs.

Run via `make export-openapi`; commit the updated openapi.json with your change.
"""

import json
from pathlib import Path

from app.main import app

OUT = Path("openapi.json")


def main() -> None:
    schema = app.openapi()
    OUT.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT} ({len(schema['paths'])} paths)")


if __name__ == "__main__":
    main()
