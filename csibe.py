#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

class CSiBEBuilder(object):

    def __init__(self, csibe_path, build_path, toolchain_name):

        self.csibe_dir = csibe_path
        self.build_dir = build_path
        self.toolchain_name = toolchain_name

        self.toolchain_build_dir = os.path.join(
                                       self.build_dir,
                                       self.toolchain_name)

        self.toolchain_files_dir = os.path.join(
                                       self.csibe_dir,
                                       "toolchain-files")

        if self.toolchain_name == "native":
            self.toolchain_file_path = None
        else:
            self.toolchain_file_path = os.path.join(
                                           self.toolchain_files_dir,
                                           "{}.cmake".format(toolchain_name))

        self.cmake_toolchain_options = ""
        if self.toolchain_file_path:
            self.cmake_toolchain_options = "-DCMAKE_TOOLCHAIN_FILE={}".format(self.toolchain_file_path)

    def run_cmake(self):
        if not os.path.isdir(self.toolchain_build_dir):
            os.makedirs(self.toolchain_build_dir)

        cmake_return_value = subprocess.call(
            ["cmake",
             self.cmake_toolchain_options,
             self.csibe_dir,
             "-B{}".format(self.toolchain_build_dir)])

        return cmake_return_value

    def run_make(self, jobs):
        return subprocess.call(
            ["make",
             "-C{}".format(self.toolchain_build_dir),
             "-j{}".format(jobs)])

    def run_make_size(self):
        return subprocess.call(
            ["make",
             "-C{}".format(self.toolchain_build_dir),
             "size"])


if __name__ == "__main__":

    toolchains = ["native",
                  "clang-cortex-m0",
                  "clang-cortex-m4",
                  "gcc-cortex-m0",
                  "gcc-cortex-m4"]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="number of jobs for make")

    parser.add_argument(
        "--toolchain",
        choices=toolchains,
        default="native",
        help="Toolchain to be used by CMake. Possible values are " + ", ".join(toolchains),
        metavar="")

    parser.add_argument(
        "--build-all",
        action="store_true",
        help="build every target")

    args = parser.parse_args()

    csibe_path = os.path.dirname(os.path.realpath(__file__))

    if args.build_all:
        targets_to_build = toolchains
    else:
        targets_to_build = [args.toolchain]

    for target in targets_to_build:
        builder = CSiBEBuilder(csibe_path, "build", target)

        cmake_return_value = builder.run_cmake()
        if cmake_return_value:
            sys.exit(cmake_return_value)

        make_return_value = builder.run_make(args.jobs)
        if make_return_value:
            sys.exit(make_return_value)

        make_size_return_value = builder.run_make_size()
        if make_size_return_value:
            sys.exit(make_size_return_value)

