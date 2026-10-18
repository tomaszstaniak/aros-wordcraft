#!/usr/bin/env python3
"""Summarizes WORDCRAFT_PERF CSVs per segment (see drive.py for the segments).

usage: summarize.py PERF_CSV[:HOST_LOG] [PERF_CSV[:HOST_LOG] ...]

With one file: per segment, frames, guest (and host) duration, the share of
the frames' work per phase, per-phase median and p90, page renders, texture
upload, event latency, the GUI rasterizer by kind of triangle, the repaint
schedule and the repaint causes (from PERF_CSV's .causes.csv when present).
With several files (repetitions of one configuration): the same segments
pooled, plus a per-run line of the typing latency, so runs can be compared.
"""
import csv
import json
import statistics
import sys
from pathlib import Path

PHASES = ["input_us", "logic_us", "ui_us", "tess_us", "textures_us", "raster_us", "blit_us"]
NAMES = {0: "startup", 1: "idle", 2: "mouse", 3: "scroll", 4: "typing", 5: "idle-after"}
KINDS = ["page", "solid", "atlas"]


def pct(values, p):
    if not values:
        return 0
    values = sorted(values)
    return values[min(len(values) - 1, int(round(p / 100 * (len(values) - 1))))]


def ms(us):
    return f"{us / 1000:.1f}"


def load(arg):
    path, _, host_path = arg.partition(":")
    rows = [{k: int(v) for k, v in r.items()} for r in csv.DictReader(open(path))]
    host = {}
    if host_path:
        marks = [json.loads(line) for line in open(host_path)]
        seg = [m for m in marks if m["what"] in ("segment", "end")]
        for a, b in zip(seg, seg[1:]):
            host[a["n"]] = (b["t"] - a["t"], a.get("frontmost"))
    causes = {}
    cpath = Path(path).with_suffix(".causes.csv")
    if cpath.exists():
        for r in csv.DictReader(open(cpath)):
            causes.setdefault(int(r["segment"]), []).append((int(r["frames"]), r["cause"]))
    return path, rows, host, causes


def segment_report(s, fr, host, causes):
    work = [sum(r[p] for p in PHASES) for r in fr]
    total = sum(work) or 1
    guest_s = (fr[-1]["at_us"] - fr[0]["at_us"]) / 1e6 if len(fr) > 1 else 0
    h = host.get(s) if host else None
    print(f"== segment {s} {NAMES.get(s, '')}: {len(fr)} frames, guest {guest_s:.1f} s"
          + (f", host {h[0]:.1f} s, frontmost {h[1]}" if h else "")
          + f", window {fr[0]['width']}x{fr[0]['height']}")
    print(f"   frame work: median {ms(statistics.median(work))} ms, p90 {ms(pct(work, 90))} ms, max {ms(max(work))} ms;"
          f" asleep median {ms(statistics.median(r['wait_us'] for r in fr))} ms")
    print("   " + "  ".join(f"{p[:-3]} {100 * sum(r[p] for r in fr) / total:.0f}% (med {ms(statistics.median(r[p] for r in fr))})" for p in PHASES))
    renders = sum(r["page_renders"] for r in fr)
    print(f"   page renders {renders} ({ms(sum(r['page_render_us'] for r in fr))} ms total, inside ui);"
          f" texture upload {sum(r['texture_px'] for r in fr) / 1e6:.2f} Mpx; vertices median {statistics.median(r['vertices'] for r in fr):.0f}")
    if "clear_us" in fr[0]:
        n = len(fr)
        raster = sum(r["raster_us"] for r in fr) or 1
        print(f"   raster per frame: clear {ms(sum(r['clear_us'] for r in fr) / n)} ms, runs {sum(r['runs'] for r in fr) / n:.0f}")
        for k in KINDS:
            g = lambda f: sum(r[f"{k}_{f}"] for r in fr) / n  # noqa: E731
            print(f"     {k:5}: {ms(g('us'))} ms ({100 * g('us') * n / raster:.0f}% of raster), {g('triangles'):.0f} tris,"
                  f" visited {g('visited') / 1e3:.0f} kpx, covered {g('covered') / 1e3:.0f} kpx,"
                  f" bilinear {g('bilinear') / 1e3:.0f} k, nearest {g('nearest') / 1e3:.0f} k,"
                  f" blended {g('blended') / 1e3:.0f} k, opaque {g('opaque') / 1e3:.0f} k"
                  + (f", {1000 * g('us') / max(g('covered'), 1):.2f} ns/covered px" if g('covered') else ""))
        timeouts = [r for r in fr if r["woke_by_event"] == 0]
        late = [r["late_us"] for r in fr if r["late_us"] >= 0]
        delays = [r["next_delay_ms"] for r in fr]
        print(f"   repaint: woke by timeout {len(timeouts)}/{n}, timeout median {statistics.median(r['wait_timeout_ms'] for r in fr):.0f} ms,"
              f" due-and-late {len(late)}/{n} (late median {ms(statistics.median(late)) if late else '-'} ms),"
              f" next delay requested: none {delays.count(-1)}, 0 ms {delays.count(0)}, "
              f"other median {statistics.median([d for d in delays if d > 0]) if any(d > 0 for d in delays) else '-'} ms")
    for frames, cause in sorted(causes.get(s, []), reverse=True)[:6]:
        print(f"     cause x{frames}: {cause}")
    ev = [r for r in fr if r["events"] > 0]
    if ev:
        print(f"   events {sum(r['events'] for r in fr)} (moves {sum(r['moves'] for r in fr)}, keys {sum(r['keys'] for r in fr)},"
              f" wheel {sum(r['wheels'] for r in fr)}) in {len(ev)} frames; latency oldest median {ms(statistics.median(r['latency_max_us'] for r in ev))} ms,"
              f" p95 {ms(pct([r['latency_max_us'] for r in ev], 95))} ms, max {ms(max(r['latency_max_us'] for r in ev))} ms")


def main():
    runs = [load(a) for a in sys.argv[1:]]
    if len(runs) == 1:
        _, rows, host, causes = runs[0]
        for s in sorted({r["segment"] for r in rows}):
            segment_report(s, [r for r in rows if r["segment"] == s], host, causes)
        return
    for path, rows, host, _ in runs:
        typing = [r["latency_max_us"] for r in rows if r["segment"] == 4 and r["keys"] > 0]
        idle = [sum(r[p] for p in PHASES) for r in rows if r["segment"] == 1]
        # Guest seconds per host second over segments 1-4: well below 1 means the emulator
        # itself ran slow during the run (host side), which scales every phase.
        ratio = ""
        if host:
            g = sum((lambda s: (s[-1] - s[0]) / 1e6 if len(s) > 1 else 0)([r["at_us"] for r in rows if r["segment"] == n]) for n in (1, 2, 3, 4))
            hs = sum(host[n][0] for n in (1, 2, 3, 4) if n in host)
            ratio = f"; guest/host {g / hs:.2f}" + (" (emulator slowed)" if g / hs < 0.8 else "")
        print(f"{Path(path).name}: typing latency median {ms(statistics.median(typing))} ms, p95 {ms(pct(typing, 95))} ms"
              f" ({len(typing)} frames); idle frame work median {ms(statistics.median(idle))} ms{ratio}")
    pooled = [r for _, rows, _, _ in runs for r in rows]
    causes = {}
    for _, _, _, c in runs:
        for s, lst in c.items():
            causes.setdefault(s, []).extend(lst)
    print(f"-- pooled over {len(runs)} runs")
    for s in sorted({r["segment"] for r in pooled}):
        segment_report(s, [r for r in pooled if r["segment"] == s], None, causes)


if __name__ == "__main__":
    main()
