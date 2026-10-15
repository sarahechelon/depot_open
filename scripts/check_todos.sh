#!/usr/bin/env sh
# Tech-debt policy: every TODO/FIXME must link an issue, e.g. TODO(DEPOT-42).
status=0
for f in $(git ls-files '*.py'); do
    grep -nE '(TODO|FIXME)(\([^)]*\))?:?' "$f" | grep -vE '\((DEPOT-[0-9]+)\)' | while IFS=: read -r line text; do
        echo "ERROR: $f:$line: TODO/FIXME must reference an issue like TODO(DEPOT-42)." >&2
    done
    if grep -nE '(TODO|FIXME)(\([^)]*\))?:?' "$f" | grep -qvE '\((DEPOT-[0-9]+)\)'; then
        status=1
    fi
done
exit $status
