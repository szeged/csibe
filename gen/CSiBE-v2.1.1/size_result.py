#!/usr/bin/env python3

import os
import subprocess

if __name__ == "__main__":

    csibe_binary_dir = os.environ["CSiBE_BIN_DIR"]
    project_binary_dir = os.environ["PROJECT_BINARY_DIR"]

    dump_obj_size_script = os.path.join(csibe_binary_dir, "dump_obj_size")

    for file in os.listdir(project_binary_dir):
        subprocess.call([dump_obj_size_script, file, project_binary_dir])
