# WordCraft 0.7.0 for AROS — ABIv11 test 4 (OpenGL)

WordCraft is a word processor that reads and writes Word documents (DOCX), and also opens and saves ODT, RTF, HTML, Markdown and plain text, and exports PDF. The archive includes two programs for x86_64 AROS:

- **WordCraft**: the editor.
- **wordcraft-cli**: a command-line tool. It converts documents, prints their text and details, renders pages to PNG, runs editing commands and serves an MCP automation interface over standard input and output.

This is an early test build. The target is AROS x86_64 ABIv11. This variant draws the interface with OpenGL through gl.library. How fast that is depends on the machine's OpenGL: with a CPU-only OpenGL it is slower than the regular test 4 build.

## Requirements

- AROS x86_64 ABIv11.
- About 160 MB of disk space. RAM use depends on the document.
- gl.library (OpenGL), which the system provides; without it the editor does not start. Use the regular test 4 build then.
- No extra libraries. Both programs use only libraries that come with AROS, and nothing in the system is replaced or added.

## Installation

Unpack the archive into any drawer, for example `Work:`:

    UnZip WordCraft-0.7.0-test4-gl.x86_64-aros-v11.zip -d Work:

This creates the drawer `Work:WordCraft` and its icon. To remove WordCraft, delete that drawer and its icon. WordCraft keeps its settings, your user dictionary and added fonts in `WordCraftData` inside its own drawer; set the variable `WORDCRAFT_CONFIG_DIR` to keep them elsewhere.

## Starting the editor

The window title ends in `[GL]`. If OpenGL cannot be used, the editor draws with the CPU instead and works as usual.


Double-click the **WordCraft** icon. The icon gives the program the stack it needs (4,000,000 bytes).

From a Shell, set the stack first:

    Stack 4000000
    Work:WordCraft/WordCraft
    Work:WordCraft/WordCraft "Work:Documents/letter.docx"
    Work:WordCraft/WordCraft --sample

Files named on the command line are opened at start; `--sample` opens a sample document. Open, Save As, Export and Insert Picture use the standard file requester. To close WordCraft, use the window's close gadget; with unsaved changes it asks first.

## Command line

`wordcraft-cli` sets up the stack it needs itself:

    wordcraft-cli info letter.docx
    wordcraft-cli text letter.docx
    wordcraft-cli convert letter.docx letter.pdf
    wordcraft-cli render letter.docx page1.png --page 1
    wordcraft-cli --help

`convert` writes the format given by the output name's extension (docx, odt, rtf, html, md, txt, pdf, png and others).

`wordcraft-cli mcp` runs an MCP server on standard input and output for an MCP client that starts it as a child process. It works on its own documents, not on the one open in the WordCraft window. Use `--automation-read-root` and `--automation-write-root` to limit which drawers it may read and write.

## Known limitations

- Printing is not available; export to PDF instead.
- Text can be copied and pasted through the clipboard; pictures cannot.
- Files dropped on the window are not opened.
- The interface does not follow a system light or dark theme; choose it in File › Options.
- F12 and Alt key shortcuts for the File tab do not work; click File instead.

## Measuring speed (for testers)

To record how long each part of drawing takes on your machine:

    Stack 4000000
    SetEnv WORDCRAFT_PERF RAM:wordcraft-perf.csv
    Work:WordCraft/WordCraft --sample

Use the editor as usual (typing, scrolling, moving the mouse), then close it with the close gadget. The file `RAM:wordcraft-perf.csv` is written when the program ends; please send it together with your machine's CPU and graphics card. While `WORDCRAFT_PERF` is set, F9 marks the start of the next part of the test (for example: press F9, wait, press F9, type a sentence); it does nothing else. `UnSetEnv WORDCRAFT_PERF` turns the recording off.

## Licenses

WordCraft is licensed under the MIT license or the Apache License 2.0, at your option. The `Licenses` drawer holds these licenses, the notices for the fonts and word lists built into the programs, the notices for the AROS and Rust libraries linked into them, and the licenses of every Rust package they contain. `SOURCE.txt` names the exact sources; the source archive of this build holds the recipe and every change made for AROS.
