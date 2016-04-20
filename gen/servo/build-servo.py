#!/usr/bin/python

import sys
import subprocess
import os

if __name__ == "__main__":
    pbdir = os.environ["PROJECT_BINARY_DIR"]
    psdir = os.environ["PROJECT_SOURCE_DIR"]
    pgdir = os.environ["PROJECT_GEN_DIR"]

    if not pbdir or not psdir or not pgdir:
        sys.exit(1)

    # For build directories
    if "SERVO_CACHE_DIR" not in os.environ:
        os.environ["SERVO_CACHE_DIR"] = os.path.join(pbdir, ".servo")

    if "CARGO_HOME" not in os.environ:
        os.environ["CARGO_HOME"] = os.path.join(pbdir, ".cargo")

    if "CARGO_TARGET_DIR" not in os.environ:
        os.environ["CARGO_TARGET_DIR"] = os.path.join(pbdir, "target")

    # Use wrappers for compilers (native)
    if "CC" not in os.environ:
        os.environ["CC"] = "gcc"

    if "CXX" not in os.environ:
        os.environ["CXX"] = "c++"

    if os.getenv("CSiBE_DEBUG", "") == "1":
        mach_debug = ["-v"]
    else:
        mach_debug = []

    subprocess.call([os.path.join(psdir, "mach"), "bootstrap-rust"])
    subprocess.call([os.path.join(pgdir, "setup-csibe.py"), os.path.join(pbdir, ".servo")])
    subprocess.call([os.path.join(psdir, "mach"), "bootstrap-cargo"])
    subprocess.call([os.path.join(psdir, "mach"), "build", "-r"] + mach_debug)
