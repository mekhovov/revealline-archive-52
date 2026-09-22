# Read-only hosted public byte audit

This audit-only feature branch does not change deployed archive main. The public audit is restricted to manual dispatch on `codex/audit-archive52-http`; the original build and deploy jobs are false on that ref. No source/release/tag/asset or Pages write action is run.

The existing fixed bounded auditor and reviewed actual-deployment originals are copied byte-for-byte from the coordinator-reviewed local request. A nested checkout holds actual deployed source `2dd7e8a598d8e37af063933733b8dc458ea9d44f`, tree `b21a8bdf97a7b4af190f065286d470e2c73e1f4f`. The audit checks 1063 canonical HTTP bodies / 590419655 bytes, including SHA-256, sizes, MIME and final URLs. It streams bodies without persisting payloads and retains each attempt, including failures.

The local first attempt failed before HTTP requests because the unchanged 1 GiB local free-space guard refused the shared disk. That failure is preserved; the hosted run retains the same guard, not a bypass. Automated suites remain waived; public byte verification is not a browser/gameplay/offline pass.
