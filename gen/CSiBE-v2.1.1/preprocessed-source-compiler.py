#!/usr/bin/env python

import argparse
import os
import subprocess

if __name__ == "__main__":

    # Use wrappers for compilers (native)
    c_compiler_name = "gcc"

    if "CC" in os.environ:
       c_compiler_name = os.environ["CC"] 

    preprocessed_sources = ""

    if "CSIBE_PREPROCESSED_SOURCES" in os.environ:
        preprocessed_sources = os.environ["CSIBE_PREPROCESSED_SOURCES"].split()

    compiler_preprocessed_flags = ["-x",
                                   "cpp-output",
                                   "-c"]

    compiler_additional_flags = ["-fno-builtin"]

    if c_compiler_name.endswith("g++") or c_compiler_name.endswith("clang++"):
        compiler_additional_flags.extend(os.getenv("CSiBE_CXXFLAGS", "").split())
    elif c_compiler_name.endswith("gcc") or c_compiler_name.endswith("clang"):
        compiler_additional_flags.extend(os.getenv("CSiBE_CFLAGS", "").split())

    compiler_call_list = [c_compiler_name]
    compiler_call_list.extend(compiler_preprocessed_flags)
    compiler_call_list.extend(compiler_additional_flags)

    for source_path in preprocessed_sources:
        actual_call_list = compiler_call_list
        actual_call_list.append(source_path)
        subprocess.call(compiler_call_list)
