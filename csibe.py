#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
import tarfile
import textwrap
import urllib2

class CSiBEBuilder(object):

    def __init__(self, csibe_path, build_path, toolchain_name, projects, flags):

        self.csibe_dir = csibe_path
        self.build_dir = build_path
        self.toolchain_name = toolchain_name
        self.projects = projects

        self.cflags = []
        self.cxxflags = []
        self.rustcflags = []

        if flags["cflags"]:
            self.cflags.extend(flags["cflags"])

        if flags["cxxflags"]:
            self.cxxflags.extend(flags["cxxflags"])

        if flags["rustcflags"]:
            self.rustcflags.extend(flags["rustcflags"])

        if flags["globalflags"]:
            self.cflags.extend(flags["globalflags"])
            self.cxxflags.extend(flags["globalflags"])
            self.rustcflags.extend(flags["globalflags"])

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

        if self.projects:
            os.environ["CSiBE_SUBPROJECTS"] = " ".join(self.projects);

        if self.cflags:
            os.environ["CSiBE_CFLAGS"] = " ".join(self.cflags);

        if self.cxxflags:
            os.environ["CSiBE_CXXFLAGS"] = " ".join(self.cxxflags);

        if self.rustcflags:
            os.environ["CSiBE_RUSTCFLAGS"] = " ".join(self.rustcflags);

    def run_cmake(self):
        return subprocess.call(
            ["cmake",
             self.cmake_toolchain_options,
             self.csibe_dir,
             "-B{}".format(self.toolchain_build_dir)])

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


def submodule_init_and_update(repository_path):
    init_return_value = subprocess.call(
                            ["git",
                             "-C",
                             repository_path,
                             "submodule",
                             "init"])

    if init_return_value:
        sys.stdout.write("Warning: Failed to execute git submodule init.")
        return

    update_return_value = subprocess.call(
                              ["git",
                               "-C",
                               repository_path,
                               "submodule",
                               "update"])

    if update_return_value:
        sys.stdout.write("Warning: Failed to execute git submodule update.")
        return


def download_old_testbed(version):
    old_csibe_tar_filename = "{}.tar.gz".format(version)
    old_csibe_dirname = os.path.join(csibe_path, "src", version)
    old_csibe_tar_filepath = os.path.join(old_csibe_dirname, old_csibe_tar_filename)
    old_csibe_extracted_dirname = os.path.join(old_csibe_dirname, "CSiBE")

    if os.path.isfile(old_csibe_tar_filepath):
        sys.stdout.write("{} has already been downloaded.\n".format(version))
    else:
        if not os.path.isdir(old_csibe_dirname):
            os.makedirs(old_csibe_dirname)

        sys.stdout.write("Downloading {}...\n".format(version))
        response = urllib2.urlopen("http://www.csibe.org/old/down.php?id=11")
        response_data = response.read()

        with open(old_csibe_tar_filepath, "wb") as code:
            code.write(response_data)

        sys.stdout.write("Done downloading {}.\n".format(version))

    if os.path.isdir(old_csibe_extracted_dirname):
        sys.stdout.write("{} has already been extracted.\n".format(version))
    else:
        sys.stdout.write("Extracting {}...\n".format(version))
        old_csibe_tar_opened = tarfile.open(old_csibe_tar_filepath)
        old_csibe_tar_opened.extractall(path=old_csibe_dirname)
        old_csibe_tar_opened.close()

        sys.stdout.write("Done extracting {}.\n".format(version))


if __name__ == "__main__":

    old_csibe_version = "CSiBE-v2.1.1"

    toolchains = ["native"]
    for item in os.listdir("toolchain-files"):
        if item.endswith(".cmake"):
            toolchains.append(item[:-6])

    projects = []
    for item in os.listdir("src"):
        if item == old_csibe_version:
            continue
        if os.path.isdir(os.path.join("gen", item)):
            projects.append(item)
    projects.append(old_csibe_version)

    helpProjects = "\navailable project names:\n\t" + "\n\t".join(projects)
    helpToolchains = "\n\navailable toolchain files:\n\t" + "\n\t".join(toolchains)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(helpProjects + helpToolchains))

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

    parser.add_argument(
        "--cmake-only",
        action="store_true",
        help="run CMake only")

    parser.add_argument(
        "--build-dir",
        default="build",
        help="directory name for build files")

    parser.add_argument(
        "--cflags",
        action="append",
        help="compiler flags for C files")

    parser.add_argument(
        "--cxxflags",
        action="append",
        help="compiler flags for CXX files")

    parser.add_argument(
        "--rustcflags",
        action="append",
        help="compiler flags for Rust files")

    parser.add_argument(
        "--globalflags",
        action="append",
        help="compiler flags for CXX files")

    parser.add_argument(
        "option",
        nargs="*",
        help="can be project names, toolchain files, or compiler flags")

    parser.add_argument(
        "--debug",
        action="store_true",
        help="turn on debug mode")

    args, global_flags = parser.parse_known_args()

    if args.globalflags:
        global_flags.append(args.globalflags)

    csibe_path = os.path.dirname(os.path.realpath(__file__))

    if args.debug:
        os.environ["CSiBE_DEBUG"] = os.getenv("CSiBE_DEBUG", "1")
        os.environ["CSiBE_DEBUG_FILE"] = \
            os.getenv("CSiBE_DEBUG_FILE", \
                      os.path.join(os.path.abspath(args.build_dir), "csibe-debug.log"))

    submodule_init_and_update(csibe_path)

    # Target selection
    targets_to_build = []
    for opt in args.option:
        if opt in toolchains:
            targets_to_build.append(opt)

    if not targets_to_build:
        if args.build_all:
            targets_to_build = toolchains
        else:
            targets_to_build = [args.toolchain]

    # Project selection
    projects_to_build = []
    for opt in args.option:
        if opt in projects:
            if opt == old_csibe_version:
                download_old_testbed(old_csibe_version)
            projects_to_build.append(opt)

    for target in targets_to_build:
        builder = CSiBEBuilder(csibe_path, args.build_dir, target, projects_to_build,
            {"cflags" : args.cflags,
             "cxxflags" : args.cxxflags,
             "rustcflags" : args.rustcflags,
             "globalflags" : global_flags})

        cmake_return_value = builder.run_cmake()
        if cmake_return_value:
            sys.exit(cmake_return_value)

        if args.cmake_only:
            continue

        make_return_value = builder.run_make(args.jobs)
        if make_return_value:
            sys.exit(make_return_value)

        make_size_return_value = builder.run_make_size()
        if make_size_return_value:
            sys.exit(make_size_return_value)

