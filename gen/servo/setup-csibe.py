#!/usr/bin/python3

import fnmatch
import os
import sys
import shutil

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(1)

    path = sys.argv[1]

    matchdir = None
    match = None
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "rustc"):
            matchdir = root
            match = os.path.join(root, filename)
            break

    if not match:
        sys.exit(1)

    scriptdir = os.getenv("CSiBE_BIN_DIR", os.path.dirname(os.path.realpath(__file__)))
    wrapper = os.path.join(scriptdir, "rustc-wrapper.py")

    original = match + "-orig"
    if os.path.isfile(original):
        sys.exit(0)

    os.rename(match, original)
    os.symlink(wrapper, match)

    for compiler in ["cc", "c++", "gcc", "g++", "clang", "clang++"]:
        target = os.path.join(matchdir, compiler)
        if not os.path.isfile(target):
            os.symlink(os.path.join(scriptdir, "compiler.py"), target)
