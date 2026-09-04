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

The sealed baseline passed the following serial contract chain with no retries:

```text
P00 -> D01 -> C13 -> L01 -> C03 -> C04 -> C05
```

The acceptance used strict original-response bytes and deterministic validators.
The result establishes compatibility with those frozen contracts; it does not
prove general scientific correctness or research validity.

## Local verification

Run either included verifier after cloning. A valid result requires:

- exactly 110 payload files;
- no missing or additional payload paths;
- all sizes and file hashes matching;
- the normalized digest matching `governance/RELEASE.json`;
- no symbolic links in the payload.
