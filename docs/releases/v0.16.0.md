# WordCraft 0.16.0 for AROS

The AROS port of WordCraft 0.16.0, a word processor that reads and writes DOCX, opens and saves ODT, RTF, HTML, Markdown, LaTeX and plain text, imports legacy DOC and exports PDF. It is built from the WordCraft 0.16.0 release (tag `v0.16.0` of 2026-11-06), for three AROS systems.

## Downloads

| File | System |
|---|---|
| `WordCraft-0.16.0-r1-aros-x86_64-abiv11-pc.zip` | AROS x86_64, ABIv11 (AROS One 1.3) |
| `WordCraft-0.16.0-r1-aros-x86_64-abiv1-pc.zip` | AROS x86_64, mainline ABIv1 (nightly 2026-11-05) |
| `WordCraft-0.16.0-r1-aros-aarch64-abiv1-raspi.zip` | AROS on Raspberry Pi, AArch64 ABIv1 (mainline nightly 2026-11-05); not for hosted Macaros |
| `WordCraft-0.16.0-r1-source.zip` | Port sources, patches, pinned inputs and build recipe |

Each package runs only on the system it was built for. `SHA256SUMS` lists the checksums. The packages can also be installed with arospkg: `apkg install wordcraft` (the catalogue shows them as `0.16.0-aros1`).

## Packaging revision 1 (2026-11-07)

The first 0.16.0 packages (release `v0.16.0`) could not be installed with arospkg on mainline AROS and on the Raspberry Pi: their package descriptions required `crt.library`, `stdlib.library` and `m.library`, the C runtime of ABIv11, which mainline AROS does not have. apkg checks the requirements before it downloads anything, so it refused the package with "this system does not provide what the package needs". Unpacked by hand, those packages run; the programs themselves were right.

Revision 1 corrects the descriptions: the mainline x86_64 and Raspberry Pi packages now require `stdc.library`, `posixc.library` and `stdcio.library`, the libraries those programs open at start. The ABIv11 description is unchanged. The programs in all three packages are byte for byte the ones of `v0.16.0` (`BUILD.txt` in each drawer lists their hashes). If you unpacked a `v0.16.0` package by hand, there is nothing to change. The packaging now refuses a description whose requirements do not match the programs.

## What is in the port

- The WordCraft editor in one AROS window, started from Workbench or a Shell, with ASL file requesters. The program takes the stack it needs itself; no `Stack` command is required.
- `wordcraft-cli`, the command-line program (convert, text, info, render, run, mcp), in the same drawer.
- Clipboard text in both directions, in the system character set (ISO 8859-2 with a Polish locale, for example) or in UTF-8 when the text does not fit it. Letters typed with the Polish keymap arrive correctly.
- A picture on the clipboard (an ILBM from Capture, MultiView or a paint program) is pasted into the document with Ctrl+V. A damaged or oversized picture is reported and the document is left unchanged.
- Polish, Greek, Cyrillic, Chinese, Japanese and emoji text survives a round trip through DOCX and ODT byte for byte. CJK and emoji characters are shown as boxes: no such font is built in.
- The interface renderer is chosen with the `GUI_RENDERER` ToolType or the `--gui-renderer` Shell argument: `CPU` (default), `AUTO` (OpenGL when it is not Mesa's software renderer, else CPU, with the reason in `WordCraft.log`) or `GPU`.

## Changes since 0.7.0 test 7

- New base: WordCraft 0.16.0 instead of 0.7.0.
- Two new systems: mainline x86_64 ABIv1 and the Raspberry Pi.
- The program raises its own stack at start; `Stack 4000000` before a Shell start is no longer needed.
- Keyboard layouts other than ISO 8859-1 now produce the right letters; the Polish keymap was tested.
- Clipboard text is written in the system character set; pictures can be pasted from the clipboard.
- The editor exits cleanly and leaves no task behind.

## Installation

Unpack the archive for your system anywhere writable and double-click WordCraft. From a Shell, run `WordCraft [--gui-renderer CPU|AUTO|GPU] [file]`. Settings, the user dictionary, added fonts and `WordCraft.log` are kept in `WordCraftData` inside the program drawer; to upgrade, unpack the new version to a new place and move `WordCraftData` into it. The archive also holds a `.arospkg` drawer with the arospkg description; after unpacking by hand it can be deleted.

`WordCraft --version` and the first line of `WordCraft.log` name the build (`0.16.0` and the target); please include them when you report a problem.

## Known limitations

- Every change redraws the whole window, so on slow machines and in emulators the interface follows with a delay.
- No printing (export to PDF instead); files dropped on the window are not opened; pictures are not copied out to the clipboard.
- OpenGL: AROS One 1.3 and the mainline nightly have only Mesa's software renderer, so `AUTO` uses CPU there. `GPU` works but draws several times slower than CPU. Hardware OpenGL drivers have not been tested.
- Raspberry Pi: tested in an emulator only, not on a physical Pi. `GPU` opens Mesa's software renderer there and is much slower than CPU; save your work before you try it.
- Mainline x86_64: in one test session the system's list of volumes and assigns was damaged after WordCraft had run. Later sessions with the same programs did not show it, and the cause is not known. Keep your documents saved.
- CJK and emoji characters are shown as boxes; the document data is kept.
- Paste Special has not been tested on AROS. The Polish keymap was tested on ABIv11 only; other keymaps and systems were not tested with it.
- The MCP server (`wordcraft-cli mcp`) has been tested only for its handshake on AROS. No automatic updates.

Licences and notices for WordCraft and everything built into it are in the `Licenses` drawer of each package.
