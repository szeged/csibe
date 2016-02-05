#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

toolchains = ["native", "clang-cortex-m0", "clang-cortex-m4", "gcc-cortex-m0", "gcc-cortex-m4"]

parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jobs", type=int, default=1, help="number of jobs for make")
parser.add_argument("--toolchain", choices=toolchains, default="native",
                    help="Toolchain to be used by CMake. Possible values are " + ", ".join(toolchains), metavar="")
args = parser.parse_args()

make_jobs = args.jobs

csibe_path = os.path.dirname(os.path.realpath(__file__))
toolchain_path = os.path.join(csibe_path, "toolchain-files")

cmake_toolchain_option = ""
if args.toolchain != "native":
    toolchain_file = "{}.cmake".format(args.toolchain)
    cmake_toolchain_option = "-DCMAKE_TOOLCHAIN_FILE={}".format(os.path.join(toolchain_path, toolchain_file))

build_directory = os.path.join("build", args.toolchain)

if not os.path.isdir(build_directory):
    os.makedirs(build_directory)

os.chdir(build_directory)

cmake_return_value = subprocess.call(["cmake", cmake_toolchain_option, csibe_path])
if cmake_return_value:
    sys.exit(cmake_return_value)

make_return_value = subprocess.call(["make", "-j{}".format(make_jobs)])
if make_return_value:
    sys.exit(make_return_value)

make_size_return_value =  subprocess.call(["make", "size"])
if make_size_return_value:
    sys.exit(make_size_return_value)

