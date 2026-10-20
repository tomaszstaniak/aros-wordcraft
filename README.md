# WordCraft for AROS

An AROS port of [WordCraft](https://github.com/storytold/wordcraft), a word processor. It opens and saves DOCX documents and exports PDF.

## Download and run

[Download v0.7.0-test4-r2](https://github.com/tomaszstaniak/aros-wordcraft/releases/tag/v0.7.0-test4-r2) for **AROS x86_64 ABIv11**, or find `wordcraft` in the apkg catalogue. The download includes WordCraft and `wordcraft-cli`.

These builds are experimental and not optimised. They use CPU rendering and can be slow, especially in large windows.

Unpack the archive into a drawer and double-click the WordCraft icon. From a Shell, run `Stack 4000000` before starting `WordCraft`.

## Known limitations

Typing can lag, especially in a large window. Printing, image clipboard exchange and file drops are unavailable. Non-Latin-1 keyboard layouts can produce incorrect characters; existing document text is displayed correctly.

## Build from source

This repository contains source revisions, AROS patches and build scripts. See [Building](docs/development.md), [Patch workflow](docs/patching.md) and [Source revisions](upstreams.json). The window and renderer use [egui-aros](https://github.com/tomaszstaniak/egui-aros), pinned in `upstreams.json`.

The repository stores build recipes rather than a full upstream source tree. Licenses and author notices are included in the source and application archives.
