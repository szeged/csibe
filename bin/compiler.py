#!/usr/bin/python3

import sys
import subprocess
import os
from csibe import logger

if __name__ == "__main__":
    def which_next(program, old):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.abspath(os.path.join(path, program))
            if is_exe(exe_file) and exe_file != old:
                return exe_file
        return None

    optflags = ["-O", "-O0", "-O1", "-O2", "-O3", "-O4", "-Os", "-Oz"]

    basename = os.path.basename(sys.argv[0])
    abspath = os.path.abspath(sys.argv[0])
    next = which_next(basename, abspath);
    if not next:
        logger.error("Missing '%s' from PATH!" % basename)
        sys.exit(1)

    clearopts=False
    if basename.endswith("g++") or basename.endswith("clang++"):
        flags = os.getenv("CSiBE_CXXFLAGS", "").split()
        ext = [".cxx", ".cpp"]
    elif basename.endswith("rustc"):
        flags = os.getenv("CSiBE_RUSTCFLAGS", "").split()
        ext = [".rs"]
    else:
        flags = os.getenv("CSiBE_CFLAGS", "").split()
        ext = [".c"]

    if flags and flags[0] == "!":
        clearopts = True
        flags = flags[1:]

    done = False
    srcfile = False

    cmd = [next]

    for arg in sys.argv[1:]:
        if "--" == arg:
            cmd.extend(flags)
            done = True
        elif [elem for elem in ext if elem in arg]:
            srcfile = True

        if (not clearopts) or (arg not in optflags):
            cmd.append(arg)

    if srcfile:
        if not done:
            cmd.extend(flags)
    else:
        cmd = [next]
        cmd.extend(sys.argv[1:])

    logger.debug("[Executing] %s" % " ".join(cmd))
    sys.exit(subprocess.call(cmd))
