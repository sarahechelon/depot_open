#!/usr/bin/env sh
# Fail if any tracked Python file exceeds MAX_LINES lines.
MAX_LINES=500
status=0
for f in $(git ls-files '*.py'); do
    lines=$(wc -l < "$f")
    if [ "$lines" -gt "$MAX_LINES" ]; then
        echo "ERROR: $f has $lines lines (max $MAX_LINES). Split it up." >&2
        status=1
    fi
done
exit $status
