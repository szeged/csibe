#!/usr/bin/python

import sys
import subprocess
import os
from csibe import logger

if __name__ == "__main__":
    done = False
    rsfile = False
    addopts = os.getenv("CSiBE_RUSTCFLAGS","").split()

    cmd = ["%s-orig" % os.path.abspath(__file__)]

    for arg in sys.argv[1:]:
        if "--" == arg:
            cmd.extend(addopts)
            done = True
        elif ".rs" in arg:
            rsfile = True
        cmd.append(arg)

    if rsfile:
        if not done:
            cmd.extend(addopts)

    logger.debug("[Executing] %s" % " ".join(cmd))
    sys.exit(subprocess.call(cmd))
