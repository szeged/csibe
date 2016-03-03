#!/usr/bin/python

import sys
import subprocess
import os

if __name__ == '__main__':
	done = False
	rsfile = False
	addopts = os.getenv('CSiBE_RUSTCFLAGS','').split()

	cmd = ['rustc-orig']

	for arg in sys.argv[1:]:
		if "--" == arg:
			cmd.extend(addopts)
			done = True
		elif ".rs" in arg:
			rsfile = True
		cmd.append(arg)

	if rsfile:
		if not done:
			cmd.extend(addopts)
	else:
		cmd = ['rustc-orig']
		cmd.extend(sys.argv[1:])

	sys.exit(subprocess.call(cmd))