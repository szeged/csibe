#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jobs", type=int, default=1, help="number of jobs for make")
args = parser.parse_args()

make_jobs = args.jobs

csibe_path = os.path.dirname(os.path.realpath(__file__))
build_directory = "build"

if not os.path.isdir(build_directory):
    os.makedirs(build_directory)

os.chdir(build_directory)

cmake_return_value = subprocess.call(["cmake", csibe_path])
if cmake_return_value:
    sys.exit(cmake_return_value)

make_return_value = subprocess.call(["make", "-j{}".format(make_jobs)])
if make_return_value:
    sys.exit(make_return_value)

make_size_return_value =  subprocess.call(["make", "size"])
if make_size_return_value:
    sys.exit(make_size_return_value)

