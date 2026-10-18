#!/usr/bin/env python3
"""Drives one responsiveness run of the editor in a pool guest and logs host times.

The editor must already be running with WORDCRAFT_PERF set, its window
centred on the screen (the default), the pointer free. Each scenario starts
with F9, which the editor's shell counts as a segment marker:

  1 idle      nothing for IDLE seconds
  2 mouse     pointer moves around the screen centre, one every MOVE_GAP s
  3 scroll    wheel down then up over the document, one step every WHEEL_GAP s
  4 typing    Ctrl+End, then one character every KEY_GAP s
  5 idle      nothing, after the typing

Segment 0 is the start-up before the first F9. The host log has one line per
action with the host's monotonic time, so guest timings can be checked against
the host clock (guest time under TCG has been seen to run slow).

usage: drive.py VMCTL_PY HOST_LOG [--keys N]
Needs the pool session's environment (`vm.sh env`).
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

IDLE = 20
MOVE_GAP, MOVES = 0.25, 60
WHEEL_GAP, WHEELS = 0.5, 10
KEY_GAP = 0.3
TEXT = "the quick brown fox jumps over the lazy dog "


def frontmost():
    """The host's frontmost application, read only: the QEMU window's state is part of the result."""
    try:
        return subprocess.run(["osascript", "-e", 'tell application "System Events" to get name of first process whose frontmost is true'],
                              capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vmctl")
    ap.add_argument("log")
    ap.add_argument("--keys", type=int, default=40)
    args = ap.parse_args()
    # vmctl imports its sibling vm_pool.
    sys.path.insert(0, str(Path(args.vmctl).resolve().parent))
    spec = importlib.util.spec_from_file_location("vmctl", args.vmctl)
    vmctl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vmctl)
    with open(args.log, "x") as log, vmctl.VM() as vm:
        def note(what, **extra):
            log.write(json.dumps({"t": time.monotonic(), "wall": time.time(), "what": what, **extra}) + "\n")
            log.flush()

        cx, cy = vm.w // 2, vm.h // 2
        note("start", screen=[vm.w, vm.h], frontmost=frontmost())

        vm.key("f9")
        note("segment", n=1, name="idle", frontmost=frontmost())
        time.sleep(IDLE)

        vm.key("f9")
        note("segment", n=2, name="mouse", frontmost=frontmost())
        for i in range(MOVES):
            dx = (-150, 150)[i % 2] + (i % 7) * 10
            dy = (-100, 100)[(i // 2) % 2]
            vm.move(cx + dx, cy + dy)
            time.sleep(MOVE_GAP)
        vm.move(cx, cy)

        vm.key("f9")
        note("segment", n=3, name="scroll", frontmost=frontmost())
        for up in (False, True):
            for _ in range(WHEELS):
                vm.wheel(cx, cy, up, 1)
                time.sleep(WHEEL_GAP)

        vm.key("f9")
        note("segment", n=4, name="typing", frontmost=frontmost())
        vm.key("ctrl-end")
        time.sleep(2)
        for c in (TEXT * 4)[: args.keys]:
            vm.type(c)
            time.sleep(KEY_GAP)

        vm.key("f9")
        note("segment", n=5, name="idle-after", frontmost=frontmost())
        time.sleep(IDLE)
        note("end", frontmost=frontmost())


if __name__ == "__main__":
    sys.exit(main())
