# First-run onboarding and portable configuration

Run `subcult-onboard guide` for a skippable preflight, capability review, privacy
notice, preset preview, and explicit activation. `subcult-onboard skip` dismisses
it without activation; `subcult-onboard reopen` makes it available again.

Export only portable owned preferences with `subcult-onboard export FILE`.
Secrets, filesystem paths, editor commands, browser targets, location, device
identity, runtime state, and the configured Git remote are excluded. Files are
created mode 0600 using schema `subcult-portable-config` version 1.

`subcult-onboard import FILE` is read-only and reports create/conflict/unchanged
plus a plan ID. Apply with `--confirm PLAN_ID`. The input hash and schema are
revalidated, every fixed allowlisted target is backed up, and the returned
transaction can be reversed with `subcult-onboard rollback TRANSACTION`.
