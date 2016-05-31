#!/usr/bin/env python

import argparse
import os
import subprocess

if __name__ == "__main__":

    #parser = argparse.ArgumentParser()
    #parser.add_argument("preprocessed_source_path", help="preprocessed source path")
    #args = parser.parse_args()

    #preprocessed_source_dir = os.environ["PROJECT_SOURCE_DIR"]
    #preprocessed_binary_dir = os.environ["PROJECT_BINARY_DIR"]

    # Use wrappers for compilers (native)
    c_compiler_name = "gcc"
    #cxx_compiler_name = "g++"

    if "CC" in os.environ:
       c_compiler_name = os.environ["CC"] 

    #if "CXX" not in os.environ:
    #    os.environ["CXX"] = "c++"

    #compiler_preprocessed_flags = "-x cpp-output"
    #compiler_additional_flags = "-c"

    preprocessed_sources = ""

    if "CSIBE_PREPROCESSED_SOURCES" in os.environ:
        preprocessed_sources = os.environ["CSIBE_PREPROCESSED_SOURCES"].split()

    compiler_preprocessed_flags = ["-x",
                                   "cpp-output",
                                   "-c"]

    compiler_additional_flags = ["-fno-builtin"]

    compiler_call_list = [c_compiler_name]
    compiler_call_list.extend(compiler_preprocessed_flags)
    compiler_call_list.extend(compiler_additional_flags)
    #compiler_call_list.append(args.preprocessed_source_path)

    #subprocess.call([c_compiler_name, "-x", "cpp-output", "-fno-builtin", compiler_additional_flags, args.preprocessed_source_path])
    for source_path in preprocessed_sources:
        actual_call_list = compiler_call_list
        actual_call_list.append(source_path)
        subprocess.call(compiler_call_list)
