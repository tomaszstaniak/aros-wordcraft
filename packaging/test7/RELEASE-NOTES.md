# WordCraft 0.7.0 for AROS — test 7

For AROS x86_64 ABIv11. Experimental and not optimised; the window is drawn by the CPU.

## Changes since test 6

- A document opened from a Shell with a name relative to the current drawer (`WordCraft letter.docx`) is now remembered with its full path, so it opens from the Recent list after a start from Workbench or from another drawer. Entries that earlier versions stored with a short name stay as they were and may show as missing; open such a document once through the file requester.
- If WordCraft cannot lock the drawer it was started from, it now stops at once with return code 20 instead of starting with only a warning. This is a safeguard; no case is known where it happens.

The crash after closing that the test 6 notes describe as fixed was found in PdfCraft. In WordCraft no way for it to happen is known, so that change is a safeguard too.

## Installation

Unpack the archive into any drawer and double-click the WordCraft icon. From a Shell, run `Stack 4000000` before starting `WordCraft`. With apkg: `apkg install wordcraft`.

## Known limitations

- Typing still lags behind, most in a large window.
- Letters typed with a keymap for another 8-bit charset (such as the Polish one) come out as the wrong characters; text in documents is shown correctly.
- No printing (export to PDF instead), no pictures through the clipboard, no file drops.
- A file name with accented letters typed in a Shell is refused with "argument is not valid text"; use names without them.
