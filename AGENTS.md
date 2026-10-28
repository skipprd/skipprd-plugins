# AGENTS.md — skipprd-plugins

This repository is the **runtime plugin catalog** for Skippr ELT. The host engine lives in sibling [`skipprd`](https://github.com/skipprd/skipprd). Plugins speak the TCP runtime protocol in `skippr-runtime-sdk`; they MUST NOT import `skipprd` or `skippr-core`.

## Layout

Clone as siblings:

```
skipprd/
skipprd-plugins/
```

Then link the host workspace (CI does this too):

```bash
ln -sfn ../skipprd .host
```

`SKIPPR_PLUGINS_ROOT` points here. `SKIPPR_SKIPPRD_ROOT` points at the host checkout when it is not named `skipprd`.

SDK crates stay in skipprd (`crates/skippr-runtime-sdk`, iceberg writer/catalogs, object-writer). Plugin `Cargo.toml` path deps resolve through `.host/crates/…`. crates.io publish of that graph is blocked by PolyForm Shield 1.0.0.

## One design

- Plugin crate versions in `plugins/**/Cargo.toml` are immutable CDN paths (`plugins/<stem>/versions/<crate>/`).
- Host discovery SoT is `{engine-semver}/manifest-index.json` written when skipprd tags.
- Do not keep a `plugins/` tree in skipprd.

## Build / test

```bash
ln -sfn ../skipprd .host
cargo test
python3 .github/scripts/test_plugin_workspace.py
python3 .github/scripts/test_runtime_plugin_catalog.py
python3 .github/scripts/test_bump_changed_plugin_crates.py
```

## Release

skipprd product tags dispatch this repo. Bump plugin crate patches here (not in skipprd) when plugin or SDK fingerprint inputs change:

```bash
python3 .github/scripts/bump_changed_plugin_crates.py --base <last-plugin-or-engine-tag>
```
