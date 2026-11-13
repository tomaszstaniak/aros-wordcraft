---
type: guide
updated: 2026-11-12
---

# Building WordCraft for AROS

Targets, named as `<system>-<arch>-<abi>-<platform>`:

| Target | System |
|---|---|
| `aros-x86_64-abiv11-pc` | ABIv11 distributions (AROS One), x86_64 PC |
| `aros-x86_64-abiv1-pc` | mainline AROS, x86_64 PC |
| `aros-aarch64-abiv1-raspi` | native AROS on Raspberry Pi, AArch64 |

A binary built for one target does not run on another. Each target has its own toolchain,
SDK, Cargo home (`deps/<target>/`) and build directory (`build/<target>/`).

The build, packaging and update tools are shared by the Craft ports and live in egui-aros under
`tools/craft`. `scripts/craft.py` runs the snapshot of them that `scripts/tooling.json` pins (a
commit and the content hash of that directory), prepared in the ignored `build/tooling/`; it
takes the commit from the egui-aros checkout named in the local file, or from the URL in
`tooling.json` when there is none. The app's names are in `scripts/port.json`. That directory's
README describes the pin, how to change it, and `update-check`, which tries the patch series on a
newer upstream commit without changing this repository.

## What you need

- Python 3.11 or later, Git, rustup.
- Rust nightly `nightly-2026-09-01` (it reports `rustc 1.100.0-nightly (0dfb098f3 2026-08-31)`)
  with `rust-src`, and one private toolchain alias per target whose sysroot holds the AROS
  standard library source for that target. The source archive carries each source as
  `sources/rust-std-<id>.tar.xz`; `sources/INDEX.json` says which build used which. Install
  one as a new alias with

  ```
  python3 scripts/install-rust-snapshot.py sources/rust-std-<id>.tar.xz /new/sysroot/dir <alias>
  ```

  The destination and the alias must be new. The source tree hash of each build is in its
  manifest.
- Per target, an AROS C toolchain and the SDK it was made for:
  - ABIv11: x86_64 AROS GCC 10.5 and the ABIv11 SDK, plus a deadwood2/AROS checkout that
    contains commit `5376f09bc1ed0c36a12fbb096406013f8a046e89` (its `compiler/pthread` is
    rebuilt with `patches/aros-pthread`).
  - mainline ABIv1: x86_64 AROS GCC 10.5 and the mainline Developer SDK of nightly 2026-11-10.
  - Raspberry Pi: the AROS-patched Clang 20.1 for `aarch64-unknown-aros` with compiler-rt, the
    Raspberry Pi Developer SDK of nightly 2026-11-10 (its `libpthread.a` is used unchanged:
    `"pthread": "sdk"` in the local file), and a pomaros-hosted checkout at
    `3bc9359d439f9fb5655cf48924413ffe670931cc` (the C bridge of the AArch64 standard library,
    built with `patches/aros-glue`).
- The rust-aros files the release used (target template, profiles, `libc-aros`, the std
  patches) at the commit in the local file (`rust_aros_commit`): a checkout of
  [rust-aros](https://github.com/tomaszstaniak/rust-aros), or `sources/rust-aros-<commit>.tar.xz`
  in the source archive.
- An egui-aros checkout containing the commit pinned in `upstreams.json`, with its upstream
  sources prepared by its own `python3 scripts/ea.py fetch`.

## Configuration

Copy `local.example.json` (an ABIv11 example) to one ignored local file per target and fill in
the paths: `local.json` (ABIv11, the default), for example `local.v1.json` and
`local.raspi.json` for the others, each with its `"target"`. Select a file with
`WORDCRAFT_LOCAL`:

```
WORDCRAFT_LOCAL=local.v1.json python3 scripts/craft.py config
```

`craft.py config` shows where every setting comes from; environment variables `WORDCRAFT_*`
override the file. Missing paths are reported, never guessed.

For the Raspberry Pi target, `aros_gcc` is the `aarch64-aros-clang` driver (with `aros_ar` and
`aros_strip` beside it), `pomaros_hosted` the pomaros-hosted checkout and `pthread` is `sdk`.
The mainline x86_64 target needs no `aros_src`.

## Steps

1. Fetch the pinned upstreams and create the work copy:

   ```
   python3 scripts/craft.py fetch
   python3 scripts/craft.py materialize
   python3 scripts/craft.py verify
   ```

2. Fetch the locked dependencies into the target's private Cargo home (once per target):

   ```
   WORDCRAFT_LOCAL=<file> python3 scripts/craft.py deps
   ```

3. Build both programs for each target. The release profile of each target is in
   `packaging/release.json`:

   ```
   python3 scripts/craft.py build
   WORDCRAFT_LOCAL=local.v1.json python3 scripts/craft.py build
   WORDCRAFT_LOCAL=local.raspi.json python3 scripts/craft.py build
   ```

   Add `--online` if Cargo still has to download crates. Each build goes to a new
   `build/<target>/out/<date>-<id>/` with the unstripped binaries, `build.log`,
   `cargo-messages.jsonl` and `manifest.json`. The manifest records the work copy commit, the
   patch series, compiler and SDK hashes, the command, every linked package and the binary
   hashes, and checks that no symbol is left undefined. `--worktree` builds uncommitted files
   too and is recorded as such; such builds cannot be packaged. A build is not a runtime test.

   The build passes `release` from `release.json` to the programs as `WORDCRAFT_RELEASE`;
   `--version` and the log banner print it, and packaging refuses a build made under another
   release name. `--tool clip-probe` and `--tool stack-probe` build egui-aros' test programs
   for the target instead of the app.

   What the build adds around the pinned source: `patches/crates/` (rayon-core,
   parking_lot_core, getrandom, filetime, ring, tar: checked against the Cargo.lock checksums
   and the recorded patched-tree hashes), `patches/aros-pthread/` (ABIv11 only),
   `patches/aros-glue/` (Raspberry Pi only) and the panic profile of the target.

4. Commit this repository, then package each build and the sources. `APKG_PACK` names
   arospkg's `tools/apkg-pack` (or `apkg-pack.pyz`), which writes each binary archive:

   ```
   export APKG_PACK=/path/to/arospkg/tools/apkg-pack
   python3 scripts/package.py binary build/aros-x86_64-abiv11-pc/out/<id>
   python3 scripts/package.py binary build/aros-x86_64-abiv1-pc/out/<id>
   python3 scripts/package.py binary build/aros-aarch64-abiv1-raspi/out/<id>
   python3 scripts/package.py source build/aros-x86_64-abiv11-pc/out/<id> \
       build/aros-x86_64-abiv1-pc/out/<id> build/aros-aarch64-abiv1-raspi/out/<id>
   ```

   `package.py` finds each target's local file by its `target`. It writes
   `dist/WordCraft-<release>[-rN]-<target>.zip` and `dist/WordCraft-<release>[-rN]-source.zip`
   (`release` and `revision` in `release.json`; `-rN` is a packaging revision of the same
   programs, arospkg's `revision`) and adds them to `dist/SHA256SUMS`. Binary archives go
   through `apkg-pack check`, `build` and `check` with the target's catalogue description from
   `packaging/catalogue/`; it adds `.arospkg/manifest.toml` (read by `apkg-pack submit`) and
   `WordCraft/application.json` (read by `apkg run`), and every other member must come out
   byte for byte as staged. It refuses an existing or listed file, a dirty repository, a
   build from a dirty work copy, a profile other than the target's in `release.json`, binaries
   that differ from the manifest, undefined symbols, and a catalogue description whose
   `requires_system` does not match the programs: the C runtime they open at start (crt,
   stdlib and m on ABIv11; stdc, posixc and stdcio on mainline ABIv1) must be required, and
   nothing may be required that no program names. `python3 -m unittest
   tests/package/test_requirements.py` checks the three descriptions and that rule. The programs are stripped with
   `strip --strip-unneeded --remove-section .comment` only: a full strip removes relocations
   AROS applies when it loads a program. The program icon is generated from WordCraft's
   64x64 application icon with the stack and ToolTypes from `release.json`.

5. Check each archive on the host: unpack it into a new directory, compare the programs with
   the packaged hashes in `WordCraft/BUILD.txt` and run the target's `nm -u` on them (it
   must print nothing). Then test the unpacked package on the target system itself.

## Source archive

`WordCraft-<version>-source.zip` holds this repository at the packaged commit and, under
`sources/`, the pinned inputs every packaged build used: WordCraft's upstream source,
egui-aros, the rust-aros files used (target template, profiles, `libc-aros`), the AROS
`compiler/pthread` sources (ABIv11), the pomaros-hosted bridge (Raspberry Pi), the Rust standard
library source of each target and the crates.io archives of the patched crates.
`sources/INDEX.json` lists them with their hashes and, under `origins`, the repository, commit
and licence of each. The Rust std snapshots carry Rust's `COPYRIGHT-library.html` and licence
texts from the rustup toolchain whose `rustc -V` matches the build. The storytold egui and winit
forks are public Git repositories pinned in `upstreams.json`.

## The editor on AROS

`apps/wordcraft-aros` (series patch 0004) replaces the desktop app's eframe/winit window with
egui-aros: an Intuition window on the default public screen, the interface drawn by the CPU
(or OpenGL, `GUI_RENDERER`), ASL requesters for Open, Save As, Export and Insert Picture,
clipboard text in the system character set or UTF-8, pictures pasted from the clipboard, and a
start-up entry that raises the program's stack to 16 MiB. Settings, the user dictionary, added
fonts, recovery data and `WordCraft.log` live in `PROGDIR:WordCraftData` (or
`WORDCRAFT_PROFILE_DIR`); the CLI uses the same folder.

`WordCraft --screenshot FILE.png [--screenshot-frames N]` writes the window's pixels after N
frames and quits. `--window WxH` sets the inner size. `--test-steps FILE.json` drives the
editor through a scripted sequence of key, mouse, clipboard and save steps. `WORDCRAFT_LOG=file` names the log file;
`RUST_LOG=info` or `debug` raises the level. `WORDCRAFT_LOG_TASKS=1` lists the program's tasks
at exit.

## Host checks

`python3 scripts/craft.py host test -p wordcraft-aros` runs the AROS program's host tests with
the pinned egui-aros.
