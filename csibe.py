#!/usr/bin/env python

import os
import subprocess
import unittest

csibe_path = os.path.dirname(os.path.realpath(__file__))
build_directory = "build"

if not os.path.isdir(build_directory):
    os.makedirs(build_directory)

os.chdir(build_directory)

subprocess.call(["cmake", csibe_path])

