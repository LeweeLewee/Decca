# -*- coding: utf-8 -*-
"""
Rev Q frozen-carrier check
==========================

Proves that every released Rev P.5 file named in the Rev Q brief §2 is
unchanged. Run it before starting Rev Q work and again before committing;
both runs must print IDENTICAL results and exit 0.

    python mechanical/CAD/Decca_Display_Bezel_revQ_frozen_check.py

Why this is not just `sha256sum`
--------------------------------
The brief's table was produced on a Windows checkout, where git's
`core.autocrlf=true` writes text files (`.py`, `.step`) to the working tree
with CRLF line endings. Hash the same file on a Linux checkout, or on a
Windows checkout where a given text file happens to have been left with LF,
and you get a different digest for byte-identical *content*.

That is a real trap: it looks exactly like a frozen file has been tampered
with. It bit this revision once. So each file is hashed three ways — as it
sits on disk, forced to LF, and forced to CRLF — and a match on any of them
is a pass, with the rendering reported so the result is never ambiguous.
Binary files (`.f3d`, `.stl`) are hashed as-is only; line-ending translation
is meaningless for them and git does not apply it.

This checks CONTENT. It does not check that the file is the right file - for
that, `git diff --name-only origin/main HEAD` must list none of them.
"""

from __future__ import print_function

import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

# SHA-256 values exactly as published in
# mechanical/Drawings/Decca_OLED_Display_Bezel_CAD_Brief_revQ.md §2
FROZEN = [
    ("mechanical/CAD/Decca_Display_Mount_revP.f3d",
     "d69bf5373b80301f645f0ad79357090f4db45d8e425b55852bc12b1fc8e0c8ba", True),
    ("mechanical/CAD/Decca_Display_Mount_revP_fusion.py",
     "719ffd666a31278f6553dae053d480f48a33cc9aba5a48521d61fc62273d9656", False),
    ("mechanical/CAD/Decca_Display_Mount_revP_verify.py",
     "7cef57d4a6f813d858bbff466e70a67c5dc5504194e6033151b306549aa11907", False),
    ("mechanical/CAD/Rear_Display_Carrier_revP.step",
     "1b25a24d3c216646dc70a5521cae8db3d456afd7e6760505a5c304ff1a05c359", False),
    ("mechanical/STL/Rear_Display_Carrier_revP.stl",
     "ec8a4adb8e4e80f3452da2edf9d56c17e55b7aa80db075310e2af75e224c5897", True),
    ("mechanical/CAD/Decca_Display_Mount_revP_assembly.step",
     "e7d9c40d250fd23d6b8aa250b2363714c8a396772bad623746ba594173d2b24a", False),
]

# The last RELEASED bezel. Rev Q must not touch it either.
BASELINE = [
    "mechanical/CAD/Front_Bezel_revN.step",
    "mechanical/STL/Front_Bezel_revN.stl",
    "mechanical/CAD/Decca_Display_Mount_revN.f3d",
    "mechanical/CAD/Rear_Display_Carrier_revN.step",
    "mechanical/CAD/Retainer_Bar_revN.step",
    "mechanical/CAD/Decca_Display_Mount_revN_assembly.step",
]


def digests(path, binary):
    raw = open(path, "rb").read()
    out = [("as-is", hashlib.sha256(raw).hexdigest())]
    if not binary:
        lf = raw.replace(b"\r\n", b"\n")
        out.append(("LF", hashlib.sha256(lf).hexdigest()))
        out.append(("CRLF", hashlib.sha256(lf.replace(b"\n", b"\r\n")).hexdigest()))
    return out


def main():
    print("=" * 78)
    print("REV Q FROZEN-CARRIER CHECK")
    print("=" * 78)
    print("repo: %s" % ROOT)
    print("")
    bad = 0
    for rel, want, binary in FROZEN:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print("  [FAIL] MISSING   %s" % rel)
            bad += 1
            continue
        ds = digests(p, binary)
        hit = [name for name, dg in ds if dg == want]
        if hit:
            print("  [PASS] %-52s %s" % (os.path.basename(rel),
                                         "matches as %s" % hit[0]))
        else:
            bad += 1
            print("  [FAIL] %-52s NO MATCH" % os.path.basename(rel))
            print("         brief expects  %s" % want)
            for name, dg in ds:
                print("         %-6s         %s" % (name, dg))
    print("")
    print("Released Rev N bezel baseline - must also be untouched:")
    for rel in BASELINE:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print("  [    ] %-52s absent" % os.path.basename(rel))
            continue
        print("  [    ] %-52s %s"
              % (os.path.basename(rel),
                 hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] + "..."))
    print("")
    print("=" * 78)
    if bad:
        print("RESULT: %d FROZEN FILE(S) DO NOT MATCH - STOP." % bad)
        print("Rev Q must not proceed while any Rev P.5 hash differs.")
        print("=" * 78)
        return 1
    print("RESULT: all %d frozen Rev P.5 files match the Rev Q brief. FREEZE INTACT."
          % len(FROZEN))
    print("")
    print("Content only. Also confirm no frozen path appears in:")
    print("    git diff --name-only origin/main HEAD")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
