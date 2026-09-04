# Validation

## Payload identity

The stable payload is the 110-file tree under `payload/runtime-receiver`.
`governance/PAYLOAD-MANIFEST.csv` records every relative path, byte size, and
SHA-256. The normalized digest is SHA-256 over the UTF-8 encoding of manifest
rows in frozen order:

```text
relative/path|size|sha256
```

Rows are joined with a single LF and no trailing LF.

## Runtime acceptance

The `v1.0.0` sealed baseline passed the following serial contract chain with no
retries:

```text
P00 -> D01 -> C13 -> L01 -> C03 -> C04 -> C05
```

The acceptance used strict original-response bytes and deterministic validators.
`v1.0.1` changes only test-fixture and repository licensing/packaging files; it
does not change executable code, Skill instructions, Router rules, schemas, or
contracts. The `v1.0.0` runtime result is therefore retained as inherited
evidence and is not represented as a fresh `v1.0.1` model-session run. It does
not prove general scientific correctness or research validity.

## Local verification

Run either included verifier after cloning. A valid result requires:

- exactly 110 payload files;
- no missing or additional payload paths;
- all sizes and file hashes matching;
- the normalized digest matching `governance/RELEASE.json`;
- no symbolic links in the payload.

Run `python tools/audit_release.py` to additionally verify the exact Apache-2.0
license bytes, release license metadata, absence of the removed publisher
content, and byte-exact NBIB-to-RIS/BibTeX fixture conversions.
