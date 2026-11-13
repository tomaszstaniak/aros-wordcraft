# WordCraft 0.18.1 for AROS

The AROS port of WordCraft 0.18.1, a word processor that reads and writes DOCX, opens and saves ODT, RTF, HTML, Markdown, LaTeX and plain text, imports legacy DOC and exports PDF. It is built from the WordCraft 0.18.1 release (tag `v0.18.1`), for three AROS systems.

## Downloads

| File | System |
|---|---|
| `WordCraft-0.18.1-aros-x86_64-abiv11-pc.zip` | AROS x86_64, ABIv11 distributions |
| `WordCraft-0.18.1-aros-x86_64-abiv1-pc.zip` | AROS x86_64, mainline ABIv1 (nightly 2026-11-06 or later) |
| `WordCraft-0.18.1-aros-aarch64-abiv1-raspi.zip` | AROS on Raspberry Pi, AArch64 ABIv1 (mainline nightly 2026-11-06 or later) |
| `WordCraft-0.18.1-source.zip` | Port sources, patches, pinned inputs and build recipe |

Each package runs only on the system it was built for. `SHA256SUMS` lists the checksums. The packages can also be installed with the AROS package manager: `apkg install wordcraft`.

## What is new

This release moves from WordCraft 0.16.0 to WordCraft 0.18.1. For the changes in the word processor itself, see the release notes of WordCraft upstream. On the AROS side:

- The window reacts faster with the CPU renderer. Only the parts of the window that changed are drawn again, so typing, moving the pointer and the blinking cursor no longer redraw everything. In the emulators used for testing, a typical frame of a scripted session took about 0.3 s before and takes 0.01 to 0.02 s now. Changes of the whole window (scrolling, zooming, opening a dialog) are several times faster too, and still follow with a delay on slow machines.
- The `GUI_RENDERER` ToolType in the icon is now `AUTO`, as in the other Craft programs, instead of `CPU`. With Mesa's software renderer, on mainline x86_64 and on the Raspberry Pi, `AUTO` uses the CPU as before.
- On mainline x86_64, `AUTO` keeps to the CPU renderer: a program that has opened OpenGL there, even only to look at it, leaves its log file in use after it ends, and the Shell it was started from no longer redirects the output of later programs (seen on nightly 2026-11-10). `GPU` still opens OpenGL.
- The mainline x86_64 and Raspberry Pi packages are now built against the nightly 2026-11-10 and need a nightly build from 2026-11-06 or later. On older ones the programs stop with a software failure at start; update the system first, or stay with WordCraft 0.16.0 there.
- A document named when the program is started is opened the way the desktop program opens it, so a Word template starts a new document. Removing a document from the recent list is saved at once.

With the package manager: `apkg upgrade wordcraft`. Settings in `WordCraftData` are kept.

## What is in the port

- The WordCraft editor in one AROS window, started from Workbench or a Shell, with ASL file requesters. The program takes the stack it needs itself; no `Stack` command is required.
- `wordcraft-cli`, the command-line program (convert, text, info, render, run, mcp), in the same drawer.
- Clipboard text in both directions, in the system character set (ISO 8859-2 with a Polish locale, for example) or in UTF-8 when the text does not fit it. Letters typed with the Polish keymap arrive correctly.
- A picture on the clipboard (an ILBM from Capture, MultiView or a paint program) is pasted into the document with Ctrl+V. A damaged or oversized picture is reported and the document is left unchanged.
- Polish, Greek, Cyrillic, Chinese, Japanese and emoji text survives a round trip through DOCX and ODT byte for byte. CJK and emoji characters are shown as boxes: no such font is built in.
- The interface renderer is chosen with the `GUI_RENDERER` ToolType or the `--gui-renderer` Shell argument: `AUTO` (default: OpenGL when it is not Mesa's software renderer, else CPU, with the reason in `WordCraft.log`), `CPU` or `GPU`.

## Installation

Unpack the archive for your system anywhere writable and double-click WordCraft. From a Shell, run `WordCraft [--gui-renderer CPU|AUTO|GPU] [file]`. Settings, the user dictionary, added fonts and `WordCraft.log` are kept in `WordCraftData` inside the program drawer; to upgrade, unpack the new version to a new place and move `WordCraftData` into it. The archive also holds a `.arospkg` drawer with the arospkg description; after unpacking by hand it can be deleted.

`WordCraft --version` and the first line of `WordCraft.log` name the build (`0.18.1` and the target); please include them when you report a problem.

Tested on an ABIv11 distribution (AROS One 1.3), on mainline x86_64 AROS nightly 2026-11-10 and on the Raspberry Pi nightly 2026-11-10 in an emulator, not on a physical Raspberry Pi. On all three: an upgrade from 0.16.0 with the package manager (settings and a file of the user kept), then a scripted session from a Shell (opening a DOCX document, typing, Save As, undo and redo, Save), a second start and removing the package. Not repeated for 0.18.1: the hand tests of 0.16.0 (the clipboard, pasting pictures, the Polish keymap, the file requesters).

## Known limitations

- Changes of the whole window (scrolling, zooming, opening a dialog) redraw all of it; on slow machines and in emulators these follow with a delay.
- No printing (export to PDF instead); files dropped on the window are not opened; pictures are not copied out to the clipboard.
- OpenGL: where only Mesa's software renderer is present, on mainline x86_64 and on the Raspberry Pi, `AUTO` uses the CPU. `GPU` with the software renderer works but draws several times slower than CPU. Hardware OpenGL drivers have not been tested.
- Raspberry Pi: tested in an emulator only, not on a physical Pi. `GPU` opens Mesa's software renderer there and is much slower than CPU; save your work before you try it.
- Mainline x86_64: in one test session the system's list of volumes and assigns was damaged after WordCraft had run. Later sessions with the same programs did not show it, and the cause is not known. Keep your documents saved.
- CJK and emoji characters are shown as boxes; the document data is kept.
- Paste Special has not been tested on AROS. The Polish keymap was tested on ABIv11 only (with 0.16.0); other keymaps and systems were not tested with it.
- The MCP server (`wordcraft-cli mcp`) has been tested only for its handshake on AROS. No automatic updates.

Licences and notices for WordCraft and everything built into it are in the `Licenses` drawer of each package.
