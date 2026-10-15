# Depot label taxonomy
#
# Apply through the GitHub UI, or bulk-sync with:
#   gh label create <name> --color <hex> --description "<desc>" --force
#
# Priority: what order to work in.
#   P0 — incident / data loss, drop everything
#   P1 — current sprint
#   P2 — backlog, next up
#   P3 — nice to have
#
# Type: what kind of work it is.
#   bug | feature | chore | tech-debt | incident
#
# Area: which part of the service.
#   backend | api-contract | tooling | docs

labels:
  - name: P0
    color: B60205
    description: Incident or data loss; drop everything
  - name: P1
    color: D93F0B
    description: Current sprint
  - name: P2
    color: FBCA04
    description: Backlog, next up
  - name: P3
    color: 0E8A16
    description: Nice to have
  - name: type:bug
    color: EE0701
    description: Something is broken
  - name: type:feature
    color: 1D76DB
    description: New capability
  - name: type:chore
    color: C5DEF5
    description: Maintenance work
  - name: type:tech-debt
    color: FEF2C0
    description: Known shortcut to pay back
  - name: type:incident
    color: B60205
    description: Postmortem follow-up
  - name: area:backend
    color: 5319E7
    description: Services, models, migrations
  - name: area:api-contract
    color: 0B5394
    description: Router/schema/OpenAPI surface
  - name: area:tooling
    color: 767676
    description: Build, CI, developer experience
  - name: area:docs
    color: 0075CA
    description: Documentation
