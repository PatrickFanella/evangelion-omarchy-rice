# SUBCULT rice health and safe remediation

SO1-410 adds a suite-specific integrity layer alongside the existing hardware
health view. `subcult-rice-health diagnose` is always read-only. It checks version
evidence, required and recommended dependencies, user-service activity,
configured widget entry points, plugin ownership, the local start-page port when the add-on is installed,
configuration schemas, and cache freshness. Every finding contains bounded
evidence and a reason; reports exclude command output, process identity, host
identity, network identity, and configuration contents.
Script installs persist the candidate `VERSION` as private suite ownership
evidence; system packages use their package-version marker. Neither source
contains machine identity.

Use `subcult-rice-health diagnose --json` for machine-readable output. The health
bar popup consumes that exact report, so the CLI and graphical view share one
diagnostic engine. Missing systemd, sockets, state, or optional commands become
explicit unavailable states instead of invented success.

## Remediation transaction

Diagnosis never applies a repair. Only allowlisted identifiers in
`omarchy/rice-health.json` are accepted. Currently the sole automatic repair is
`quarantine-stale-health-cache`; all broader findings remain evidence-backed
manual guidance.

1. Run `subcult-rice-health preview quarantine-stale-health-cache`.
2. Review the exact operation and copy its `plan_id`.
3. Apply with `subcult-rice-health apply quarantine-stale-health-cache --confirm PLAN_ID`.
4. Restore the byte-for-byte cache backup with
   `subcult-rice-health rollback TRANSACTION_ID`.

Transactions and manifests are private (`0700` directories and `0600` JSON).
No reset, package installation, service mutation, or unowned-file repair is
available through this interface. If a transaction backup is missing or its
manifest is invalid, rollback stops without changing the target.
