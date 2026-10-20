# WordCraft for AROS

An experimental AROS x86_64 ABIv11 port of [WordCraft](https://github.com/storytold/wordcraft), a word processor.

WordCraft opens and saves DOCX documents and exports PDF. The experimental builds include the editor and `wordcraft-cli`. The newest is test 4: the editor now runs on [egui-aros](https://github.com/tomaszstaniak/egui-aros), the AROS integration shared with the PhotoCraft, DeckCraft and GridCraft ports. Typing can still lag, especially in a large window.

Unpack the archive into a drawer and double-click the WordCraft icon. From a Shell, run `Stack 4000000` before starting `WordCraft`.

Printing, pictures through the clipboard and opening files dropped onto the window are unavailable. Export to PDF for printing elsewhere. Letters typed with a keymap for another 8-bit charset (such as the Polish one) come out as the wrong characters.

## Sources and build

This repository contains the pinned source revisions, AROS patches and build scripts. See [development](docs/development.md), [patching](docs/patching.md) and [upstreams.json](upstreams.json). The build also needs a clone of egui-aros at the commit pinned there.

Upstream sources and generated build outputs are fetched or created locally. They are not included in the repository. Mainline ABIv1 is a separate target; these binaries require ABIv11.

Upstream and dependency licenses and author notices are retained in the application archives and pinned sources.
