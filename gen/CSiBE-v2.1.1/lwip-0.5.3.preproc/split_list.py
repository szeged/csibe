#!/usr/bin/env python

import os
import subprocess
import time

if __name__ == "__main__":

    preprocessed_sources = ""

    if "CSIBE_PREPROCESSED_SOURCES" in os.environ:
        preprocessed_sources = os.environ["CSIBE_PREPROCESSED_SOURCES"].split()

    print preprocessed_sources
    time.sleep(20)
