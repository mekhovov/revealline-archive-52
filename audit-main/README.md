# Read-only complete main Pages inventory audit

This fixed audit branch in the Archive52 harness repository never deploys. Manual dispatch on `codex/audit-main-v0840-b17e61d` runs only `audit-main-public-bytes` with contents-read permissions; archive build/deploy jobs are structurally false on this ref. No production/main selector, archive main, release, tag or asset mutation occurs.

The audit binds the actual completed main Pages run `35783546172`, controller `b17e61d58f23c758802f54cb929ce47c25dd5416`, tree `a0d27835d736f6a5058f372f5c17e76cc8bdcc5b`, and immutable v0.84.0 game source `1107f570508e0d107440236b6aeedbce8506cd7d`. The complete inventory is extracted from the exact GitHub-digest-verified production `frozen-pages-receipts` artifact, not inferred from a preview or subset.

The streaming loop retains the reviewed Archive52 auditor's finite limits, four workers, three bounded attempts, 1 GiB free-space guard, exact URL/no-redirect policy, content-length/size/SHA-256 and MIME checks, and every attempt. It persists reports, not public payloads. Main-origin historical bridge bytes are covered; the separate canonical inventories of all older archive sites are not re-audited here. Browser, gameplay, offline and physical-device acceptance remain separate.

Production deployment originals, final status, receipt artifact metadata/body, inventory and sparse held controller/catalog are all bound before the first HTTP request and revalidated after the final response. Automated suites are waived, not passed; public byte verification remains mandatory.
