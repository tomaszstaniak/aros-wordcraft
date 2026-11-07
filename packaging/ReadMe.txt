WordCraft @VERSION@ for AROS
==========================

WordCraft is a word processor. It reads and writes Word documents (DOCX),
opens and saves ODT, RTF, HTML, Markdown, LaTeX and plain text, imports
legacy 97-2003 DOC, and exports PDF. This is its AROS port, based on
WordCraft @UPSTREAM_VERSION@.

This package is for: @SYSTEM@.
It does not run on other AROS systems; use the package made for yours.

The drawer holds two programs:

  WordCraft       the editor
  wordcraft-cli   the command-line program: converts documents, prints
                  their text and details, renders pages to PNG, runs
                  editing scripts and serves an MCP automation interface
                  over standard input and output


Installation
------------

Unpack the archive anywhere writable, for example to Work:. It creates the
drawer WordCraft and its icon. Both programs use only libraries that come
with AROS; nothing in the system is replaced or added.

To upgrade, unpack the new version to a new place (not over the old drawer),
then move the drawer WordCraftData from the old WordCraft drawer into the
new one to keep your settings, user dictionary and added fonts.

Starting
--------

Workbench: double-click WordCraft. The program takes the stack it needs
itself; it also works from a Shell with the default stack.

Shell:

  WordCraft [--gui-renderer CPU|AUTO|GPU] [--window WxH] [file ...]
  WordCraft --sample

Files named on the command line are opened at start; --sample opens a
sample document. Open, Save As, Export and Insert Picture use the standard
file requester. To close WordCraft, use the window's close gadget; with
unsaved changes it asks first.

  wordcraft-cli info letter.docx
  wordcraft-cli text letter.docx
  wordcraft-cli convert letter.docx letter.pdf
  wordcraft-cli render letter.docx page1.png --page 1
  wordcraft-cli --help

convert writes the format given by the output name's extension (docx, odt,
rtf, html, md, tex, txt, pdf, png). wordcraft-cli mcp runs an MCP server on
standard input and output for a client that starts it as a child process;
--automation-read-root and --automation-write-root limit the drawers it
may read and write.

Settings and log
----------------

Settings, the user dictionary, added fonts, recovery data and the log file
WordCraft.log are kept in the drawer WordCraftData inside the WordCraft
drawer; it is created at the first start. The variable WORDCRAFT_PROFILE_DIR
names another drawer instead. WORDCRAFT_LOG names another log file.

Clipboard
---------

Text is exchanged with other programs through the system clipboard in the
system character set (ISO 8859-2 with a Polish locale, for example) and in
UTF-8 when the text does not fit it. A picture on the clipboard (an ILBM
written by Capture, MultiView or a paint program) is pasted into the
document with Ctrl+V. Pictures are not copied out to the clipboard.

Interface renderer
------------------

The ToolType GUI_RENDERER in the program's icon, or the Shell argument
--gui-renderer, chooses how the interface is drawn. A Shell argument takes
priority; the icon is not read when the program is started from the Shell.
Values ignore letter case.

  CPU   the processor draws the interface; OpenGL is not opened (default)
  AUTO  OpenGL if it opens and is not Mesa's software renderer, otherwise
        CPU; the reason is written to WordCraft.log
  GPU   OpenGL (the software renderer too), or the program stops with an
        error

On systems where OpenGL is Mesa's software renderer (softpipe), it is
several times slower than CPU, which is why CPU is the default.

Known limitations
-----------------

@LIMITATIONS@

Licences
--------

WordCraft is available under the MIT license or the Apache License 2.0,
at your option. The texts, the notices for the fonts and other bundled
material, and the licences of everything linked into the programs are in
the Licenses drawer. BUILD.txt identifies this build.

WordCraft: https://github.com/storytold/wordcraft
AROS port: https://github.com/tomaszstaniak/aros-wordcraft
