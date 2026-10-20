# Rejected changes

Patches tried and not taken into the series, kept with the reason.

- `0001-wordcraft-aros-read-a-texture-drawn-1-1-directly.patch` (2026-10-17, run wp4 on pool v11-1, against the series through 0010): the screenshots of the sample document changed (9717 pixels at 1008x720, at most 4 per channel: the page image is not exactly on whole texels, so bilinear filtering was smoothing it), and the one valid run per size was slower, not faster (idle frame work 1025 ms against 448 ms at 1008x720; solid fills, which the change does not touch, 444 instead of 110 ns per pixel). The slowdown's cause was not investigated. Applies on top of 0010.
