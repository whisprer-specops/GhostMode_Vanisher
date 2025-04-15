# Core Architecture

2. Threat Model

GhostMode is hardened against the following:

- Passive network surveillance (metadata/time correlation)
- Active fingerprinting (browser entropy, MACs, TLS signatures)
- Stylometry (authorship detection)
- Forensic USB traces and swap residue
- Identity crossover via logs or config bleed
- Crypto wallet leakages (e.g. Monero .keys or view-only wallets)

It does **not** protect against:

- UEFI/BIOS level malware
- Physical access keylogging
- Pre-compromised systems
- NSO-tier adversaries with upstream control

GhostMode was built to disappear from the eyes of everyone *except maybe God and Google Cloud's SIEM.*