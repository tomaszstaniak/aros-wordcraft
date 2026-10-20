# WordCraft 0.7.0 for AROS — test 4

Experimental build for x86_64 AROS ABIv11.

## Changes since test 3

- The editor now runs on a shared AROS integration for egui programs, also used by
  the PhotoCraft port. Drawing and speed are the same as in test 3.
- Amiga+C, Amiga+X and Amiga+V copy, cut and paste, like Ctrl+C, Ctrl+X and Ctrl+V.
- The window title shows the unsaved-changes mark and dashes correctly.
- Edges of translucent pictures and shadows no longer show a thin seam line.

## Installation

Unpack the archive into any drawer and double-click the WordCraft icon. From a Shell,
run `Stack 4000000` before starting the editor. Test 3 and test 4 can be
unpacked into different drawers and used side by side.

## Known limitations

- Typing still lags behind, most in a large window.
- Letters typed with a keymap for another 8-bit charset (such as the Polish one) come
  out as the wrong characters; text in documents is shown correctly.
- No printing (export to PDF instead), no pictures through the clipboard, no file drops.
