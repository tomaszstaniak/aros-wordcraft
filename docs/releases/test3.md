# WordCraft 0.7.0 for AROS — test3

Experimental build for x86_64 AROS ABIv11.

WordCraft opens and saves DOCX documents and exports PDF. This experimental build includes the editor and `wordcraft-cli`.

The editor waits when idle. Drawing solid shapes also avoids some unnecessary work. Typing can still lag, especially in a large window.

Unpack the archive into a drawer and double-click the WordCraft icon. From a Shell, run `Stack 4000000` before starting `WordCraft`.

Printing, pictures through the clipboard and opening files dropped onto the window are unavailable. Export to PDF for printing elsewhere.
