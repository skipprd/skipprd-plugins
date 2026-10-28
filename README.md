# skipprd-plugins

Runtime source, sink, and schema plugins for [skipprd](https://github.com/skipprd/skipprd).

Clone next to `skipprd`, then:

```bash
ln -sfn ../skipprd .host
cargo build -p skippr-plugin-data-source-file
```

See `AGENTS.md`.
