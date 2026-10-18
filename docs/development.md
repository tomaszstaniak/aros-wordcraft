---
type: guide
updated: 2026-10-17
---

# Development

## Current capabilities

A pinned WordCraft source plus an explicit patch series builds the editor
(`WordCraft`) and the command line (`wordcraft-cli`, including the MCP server
over stdio) for **x86_64 AROS ABIv11** with a private Rust std toolchain. Both
have been started on an ABIv11 guest (older AROS One 1.3 installation); see
"What has been run" below for the exact scope. Mainline ABIv1 is not built.

## Targets

| Architecture / ABI | Priority | Compile | Link | Runtime |
|---|---|---|---|---|
| x86_64 / ABIv11, older SDK (AROS One 1.3) | Primary | yes | yes | editor and CLI checks pass (see below) |
| x86_64 / ABIv11, 2026.09 SDK | Primary, separate profile | not run | not run | not run |
| x86_64 / mainline v1 | Secondary | not run | not run | not run |

## Requirements

- An x86_64 ABIv11 GCC 10.5 cross toolchain and the matching SDK. The C glue,
  the patched pthread objects and the Rust link must all use the same SDK:
  ABIv1 and ABIv11 pass `SysBase` differently, and a mismatch crashes inside the
  first system call instead of failing to build.
- A private Rust std toolchain for AROS registered with rustup, reporting
  exactly `rustc 1.100.0-nightly (0dfb098f3 2026-08-31)`, built with the
  rust-aros std patch tooling.
- A rust-aros checkout (target template `x86_64-aros.json.in` and
  `std-groundwork/libc-aros`, at the commit named in `scripts/wcconfig.py`).
- A deadwood2/AROS checkout containing the commit named in
  `scripts/wcconfig.py` (its `compiler/pthread` source is read, never changed).
- Python 3.11+, Git, `patch`, and network access once for `cargo fetch`.

## Configuration

`scripts/wcconfig.py` is the one place for paths. Each setting comes from an
environment variable, else the ignored `local.json` (copy
`local.example.json`), else a default. `python3 scripts/wc.py config` shows
where each value comes from; a missing value is reported with the variable that
sets it.

## Build

```sh
python3 scripts/wc.py fetch          # clone/verify upstream/wordcraft at its pin
python3 scripts/wc.py materialize    # work/wordcraft = pin + patches/wordcraft/series; never overwrites
CARGO_HOME=deps/v11/cargo-home cargo +TOOLCHAIN fetch --manifest-path work/wordcraft/Cargo.toml   # once, online
python3 scripts/wc.py build --online # once, for the std sources' own dependencies
python3 scripts/wc.py build          # WordCraft and wordcraft-cli
python3 scripts/wc.py build -p wordcraft-cli
```

Each build writes `build/v11/out/<time>-<id>/` with the binaries and
`manifest.json`: work-copy commit and dirtiness, upstream pin, crate and
libc-aros patch digests, the pthread objects, toolchain identity, the cargo
command, binary SHA-256 and a check that no symbol is left undefined. Builds use
the committed work-copy tree unless `--worktree` is given (recorded as such).
Ambient `RUSTFLAGS`, `CARGO_TARGET_DIR` and similar overrides are refused.

What the build adds around the pinned source:

- `patches/crates/`: rayon-core 1.13.0 (`terminate_global_thread_pool`) and
  parking_lot_core 0.9.12 (realtime condvar deadlines on AROS), checked against
  the Cargo.lock checksums and the recorded patched-tree hashes.
- `patches/libc-aros/`: a `memchr` declaration for rust-aros libc-aros.
- `patches/aros-pthread/`: the pthread link library's detach fix. The unpatched
  `compiler/pthread` is first rebuilt and compared with the SDK's
  `libpthread.a`, object for object; then the two patched objects go first on
  the link line (the GCC driver searches the SDK's `lib/` before any `-L`).
- `--cfg getrandom_backend="custom"`, served by the `wordcraft-aros-entropy`
  crate, which `wordcraft-docx` links on AROS.
- The unwind panic profile (`-Cpanic=unwind -Cforce-unwind-tables=yes`) by
  default; `WORDCRAFT_PANIC=abort` selects abort.

These dependency patches are the PhotoCraft AROS port's, unchanged.

Never strip the binaries fully; `x86_64-aros-strip --strip-debug` is safe.

## The editor on AROS

`apps/wordcraft-aros` replaces the desktop app's eframe/winit window. It opens
an Intuition window on the default public screen, draws the interface in
software and blits it in. File › Open, Save As, Export and Insert Picture use
ASL requesters; the chosen path is made absolute. Text copy and paste use the
system clipboard (FTXT). Settings, the user dictionary and added fonts live in
`PROGDIR:WordCraftData` (or the folder named by `WORDCRAFT_CONFIG_DIR`); the CLI
uses the same folder.

Not available in this shell: printing, pictures on the clipboard, file drops,
the control server for `wordcraft-cli mcp --connect`, the desktop theme
setting, default-app registration.

The editor needs a large stack: from a Shell, `Stack 4000000` first.
`wordcraft-cli` runs its command on a thread with an 8 MiB stack and works at
a Shell's default stack size.

`WordCraft --screenshot FILE.png [--screenshot-frames N]` writes the window's
pixels after N frames and quits. `WORDCRAFT_LOG=file` appends the log to a file
(the AROS Shell cannot redirect a program's error output); `RUST_LOG=info` or
`debug` raises the level.

## Measuring responsiveness

`WORDCRAFT_PERF=<file>` makes the editor record every pass of its event loop
in memory and write the records as CSV when it exits: time asleep, input,
`logic`, `ui`, tessellation, texture upload, rasterization and blit, the
events handled and their latency, page renders and their time. F9 is then a
segment marker and does not reach the editor. `tests/perf/drive.py` drives
idle, mouse, scroll and typing segments through the test machine's QMP
socket and logs host times; `tests/perf/summarize.py CSV [HOST_LOG]` prints
per-segment summaries.

## What has been run

On 2026-10-17, ABIv11 guest with the older AROS One 1.3 installation, QEMU TCG,
1024x768, everything from `RAM:`:

- `wordcraft-cli`: `--version`, `info`, `text`, `convert` to ODT and PDF,
  `render` of a page to PNG, `run` with commands and `--save` to DOCX, and the
  MCP server over stdio answering `initialize` and `tools/list`. The outputs
  were read back on the host (text, page count, rendered page).
- `WordCraft`: open a DOCX given on the command line, the window screenshot,
  typing, Enter, Shift+Home selection, Ctrl+B, End, a font chosen from the
  font list, Ctrl+S, File › Save As through the ASL requester into another
  directory, closing with the window's close gadget and a clean exit. The
  saved DOCX files were read back on the host with their text, bold and font.

Not run: MCP tools beyond the handshake, Open through the requester, pictures,
tables, spelling suggestions, clipboard paste from another program, large
documents, memory measurements, a start from Workbench, other ABIv11
installations, mainline v1.
