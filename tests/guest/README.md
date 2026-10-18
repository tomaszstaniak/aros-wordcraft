# Guest scripts

AmigaDOS scripts for one run on an ABIv11 guest. Put the binaries from a
build output, `tests/fixtures/hello.docx` and `mcp-in.txt` into one directory,
replace `RUN` with a new run name, unpack the directory to `RAM:wc` in the
guest and `Execute` the script. Results are new `RESULTS:<run>-*` files; the
`.rc` files hold each command's return code.

- `run-cli`: `wordcraft-cli` version, info, text, ODT/PDF/PNG output, a
  scripted edit with save, and the MCP handshake over stdio.
- `run-shot`: the editor's own window screenshot of `hello.docx`, then exit.
- `run-gui`: an interactive editor session; saves into `RAM:wc out` are listed
  and copied afterwards.

`tests/fixtures/hello.docx` was written by `wordcraft-cli run` on the host.
