# WordCraft 0.7.0 for AROS — test 6

For AROS x86_64 ABIv11. Experimental and not optimised; the window is drawn by the CPU.

## Changes since test 4

- Fixed a possible crash after closing WordCraft when it was started from Workbench. A background thread could make the C library release the starting drawer's lock that Workbench releases again on exit; the program now keeps that lock for itself.
- The programs are built with whole-program optimisation and stripped of unneeded symbols, so they are smaller.
- WordCraft is available as `wordcraft` in the apkg catalogue. It installs with apkg 0.5.0 and later.

Test 5 was withdrawn: it exited at startup with "cannot preserve the startup directory". This build fixes that.

## Installation

Unpack the archive into any drawer and double-click the WordCraft icon. From a Shell, run `Stack 4000000` before starting `WordCraft`. With apkg: `apkg install wordcraft`.

## Known limitations

- Typing still lags behind, most in a large window.
- Letters typed with a keymap for another 8-bit charset (such as the Polish one) come out as the wrong characters; text in documents is shown correctly.
- No printing (export to PDF instead), no pictures through the clipboard, no file drops.
