# WordCraft for AROS

An experimental AROS x86_64 ABIv11 port of [WordCraft](https://github.com/storytold/wordcraft), a word processor.

WordCraft opens and saves DOCX documents and exports PDF. This experimental build includes the editor and `wordcraft-cli`.

The editor waits when idle. Drawing solid shapes also avoids some unnecessary work. Typing can still lag, especially in a large window.

Unpack the archive into a drawer and double-click the WordCraft icon. From a Shell, run `Stack 4000000` before starting `WordCraft`.

Printing, pictures through the clipboard and opening files dropped onto the window are unavailable. Export to PDF for printing elsewhere.

## Sources and build

This repository contains the pinned source revisions, AROS patches and build scripts. See [development](docs/development.md), [patching](docs/patching.md) and [upstreams.json](upstreams.json).

Upstream sources and generated build outputs are fetched or created locally. They are not included in the repository. Mainline ABIv1 is a separate target; these binaries require ABIv11.

Upstream and dependency licenses and author notices are retained in the application archives and pinned sources.
