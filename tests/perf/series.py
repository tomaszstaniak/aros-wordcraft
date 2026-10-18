#!/usr/bin/env python3
"""Runs repetitions of the responsiveness scenario in one booted pool guest.

usage: series.py VMCTL_PY OUT_DIR PREFIX REPS [--port PORT]

The guest must show an AROS Shell with the payload unpacked to RAM:wc
(WordCraft, putfile and run-perf) and a running TCP/IP stack. recv.py is
started here and receives the guest's reports in OUT_DIR. For each
repetition, sizes A (1008x720) and B (640x480) alternate: run-perf starts the
editor, drive.py runs the segments, then the close gadget and "Don't Save"
end it. Names: PREFIX-a1, PREFIX-b1, ...

A run counts only when the guest has sent PREFIX-xN.done, which run-perf
sends after the editor has exited, and the report is complete: return code
0, the causes file, and measurement rows for every segment 0-5. Otherwise
the series stops at once and nothing more is typed into the guest. Needs the
pool session's environment (`vm.sh env`).
"""
import csv
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STARTUP = 75
DONE_TIMEOUT = 120
# Screen positions of the window's close gadget and of the dialog's Don't Save
# for the centred window of each size on a 1024x768 screen.
SIZES = {"a": ("1008x720", (11, 14), (579, 398)), "b": ("640x480", (203, 157), (586, 420))}


class Stop(Exception):
    pass


def vmctl(tool, *args):
    subprocess.run([sys.executable, tool, *args], check=True)


def check_report(out, name):
    """Raises Stop unless the run's report arrived complete."""
    rc = out / f"{name}.rc"
    if not rc.exists() or rc.read_text().strip() != "0":
        raise Stop(f"{name}: return code {rc.read_text().strip() if rc.exists() else 'missing'}")
    if not (out / f"{name}.causes.csv").exists():
        raise Stop(f"{name}: causes file missing")
    data = out / f"{name}.csv"
    if not data.exists():
        raise Stop(f"{name}: measurement missing")
    try:
        segments = {int(r["segment"]) for r in csv.DictReader(open(data))}
    except (ValueError, KeyError, csv.Error) as e:
        raise Stop(f"{name}: measurement unreadable: {e}")
    if segments != set(range(6)):
        raise Stop(f"{name}: segments {sorted(segments)}, expected 0-5")


def main():
    tool, out, prefix, reps = sys.argv[1], Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8765"
    out.mkdir(parents=True, exist_ok=True)
    recv = subprocess.Popen([sys.executable, str(HERE / "recv.py"), str(out), port],
                            stdout=open(out / "recv.log", "a"), stderr=subprocess.STDOUT)
    try:
        for n in range(1, reps + 1):
            for key, (size, close, dont_save) in SIZES.items():
                name = f"{prefix}-{key}{n}"
                if any(out.glob(f"{name}.*")):
                    raise Stop(f"{name}: results already present in {out}")
                print(f"{time.strftime('%H:%M:%S')} {name} {size}", flush=True)
                vmctl(tool, "type", f"Execute RAM:wc/run-perf {name} {size}", "ret")
                time.sleep(STARTUP)
                subprocess.run([sys.executable, str(HERE / "drive.py"), tool, str(out / f"{name}-host.jsonl")], check=True)
                vmctl(tool, "click", *map(str, close))
                time.sleep(6)
                vmctl(tool, "click", *map(str, dont_save))
                deadline = time.monotonic() + DONE_TIMEOUT
                while not (out / f"{name}.done").exists():
                    if time.monotonic() > deadline:
                        vmctl(tool, "shot", str(out / f"{name}-stopped.png"))
                        raise Stop(f"{name}: no done marker within {DONE_TIMEOUT} s of Don't Save; the editor has not "
                                   f"ended or the report was not sent (screenshot {name}-stopped.png)")
                    time.sleep(2)
                check_report(out, name)
                print(f"{time.strftime('%H:%M:%S')} {name} complete", flush=True)
    except Stop as e:
        print(f"series stopped: {e}", flush=True)
        return 1
    finally:
        recv.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
