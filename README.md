# WordCraft for AROS

An AROS port of [WordCraft](https://github.com/storytold/wordcraft), a word processor. It reads and writes DOCX, opens and saves ODT, RTF, HTML, Markdown, LaTeX and plain text, imports legacy DOC and exports PDF.

## Download and run

[Download 0.16.0](https://github.com/tomaszstaniak/aros-wordcraft/releases/tag/v0.16.0) for one of these systems, or install `wordcraft` with arospkg:

| Package | System |
|---|---|
| `WordCraft-0.16.0-aros-x86_64-abiv11-pc.zip` | AROS x86_64, ABIv11 (AROS One 1.3) |
| `WordCraft-0.16.0-aros-x86_64-abiv1-pc.zip` | AROS x86_64, mainline ABIv1 (nightly 2026-11-05) |
| `WordCraft-0.16.0-aros-aarch64-abiv1-raspi.zip` | AROS on Raspberry Pi, AArch64 ABIv1 (mainline nightly 2026-11-05) |

Each package runs only on the system it was built for and includes WordCraft and `wordcraft-cli`. Unpack the archive anywhere writable and double-click the WordCraft icon; from a Shell, run `WordCraft [file]`. The program takes the stack it needs itself. `ReadMe.txt` in the drawer describes installation, the command line, the clipboard and the interface renderer.

## Known limitations

The whole window is redrawn on every change, so the interface follows with a delay on slow machines and in emulators. There is no printing (export to PDF instead), no file drops and no copying of pictures out to the clipboard. CJK and emoji characters are shown as boxes. OpenGL was tested only with Mesa's software renderer, and the Raspberry Pi build only in an emulator. The [release notes](docs/releases/v0.16.0.md) list the rest.

## Build from source

This repository contains source revisions, AROS patches and build scripts. See [Building](docs/development.md), [Patch workflow](docs/patching.md) and [Source revisions](upstreams.json). The window, clipboard and start-up code use [egui-aros](https://github.com/tomaszstaniak/egui-aros), pinned in `upstreams.json`; the Rust standard library for AROS comes from [rust-aros](https://github.com/tomaszstaniak/rust-aros).

The repository stores build recipes rather than a full upstream source tree. The source archive of each release adds the pinned inputs. Licenses and author notices are included in the source and application archives.
