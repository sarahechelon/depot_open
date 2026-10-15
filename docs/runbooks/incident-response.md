# Incident response runbook

Full guide: internal wiki (Notion > Engineering > Depot). This page covers the
first 15 minutes.

## 1. Detect

- Alert sources: uptime check on `/health`, Prometheus alerts on `/metrics`
  (5xx rate, p99 latency), Sentry issues.
- On-call rotation: PagerDuty schedule "depot-primary".

## 2. Triage

```sh
curl -s https://<env>/health            # is the service up?
curl -s https://<env>/metrics | head    # error rates, latency
```

- Check the latest deployment; if regressions started right after a release,
  roll back (revert the release-please tag; the CD pipeline redeploys).

## 3. Mitigate

- Feature-flag breakage: disable the flag (`DEPOT_FLAG_*`) and redeploy; see
  `app/flags.py` and `.env.example`.
- Database issues: prefer read-only mode over data risk; do not run manual
  writes on prod. Escalate to the DBA rota.

## 4. Follow up

- File an issue using the incident template label `type:incident`.
- Post a short postmortem (timeline, cause, actions) within 3 business days.
