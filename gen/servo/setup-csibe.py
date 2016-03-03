#!/usr/bin/python

import fnmatch
import os
import sys
import shutil

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		sys.exit(1)

	path = sys.argv[1]

	match = None
	for root, dirnames, filenames in os.walk(path):
	    for filename in fnmatch.filter(filenames, 'rustc'):
	        match = os.path.join(root, filename)
	        break

	if not match:
		sys.exit(1)

	wrapper = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rustc-wrapper.py')

	original = match + "-orig"
	if os.path.isfile(original):
		sys.exit(2)

	os.rename(match, original)
	shutil.copy2(wrapper, match)
