# Security policy

MemoryGraft is research code for studying poisoned memory retrieval. The
payloads intentionally contain unsafe procedural advice. Do not run them
against production agents, production memory stores, or sensitive data.

## Reporting a vulnerability

For a vulnerability in the MemoryGraft experiment code, use this repository's
private GitHub security-advisory form. Please do not publish exploit details in
a public issue before the maintainers can assess them.

For a reproducibility bug that does not expose users or data, open a normal
GitHub issue and include the command, Python version, platform, and traceback.

The vendored `metagpt/` directory is a historical experiment dependency. Report
new vulnerabilities in upstream MetaGPT to its maintainers as well.
