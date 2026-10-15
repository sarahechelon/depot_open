#!/usr/bin/env sh
# Validate that every `make <target>` referenced in AGENTS.md/README exists in the Makefile.
# Keeps AGENTS.md commands trustworthy for agents and humans.
status=0
for doc in AGENTS.md README.md; do
    for target in $(grep -oE '`make [a-z-]+`' "$doc" | tr -d '`' | awk '{print $2}' | sort -u); do
        if ! grep -qE "^$target:" Makefile; then
            echo "ERROR: $doc references 'make $target' but '$target:' is not defined in Makefile." >&2
            status=1
        fi
    done
done
exit $status
