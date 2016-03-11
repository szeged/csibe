#!/usr/bin/python

import os
import sys
import fnmatch
import subprocess
import re

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        sys.exit(1)
    os.chdir(sys.argv[1])
    outfile = sys.argv[2]

    invalid = '-'
    res = {}
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.o'):
            matches.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, '*.rlib'):
            matches.append(os.path.join(root, filename))

    for elem in matches:
        p = subprocess.Popen(['size', elem], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        rc = p.returncode

        lines = output.split('\n')
        for line in lines:
            items = line.strip().split()
            if len(items) > 5 and items[5].endswith('.o'):
                name = os.path.basename(items[5])
                size = items[0]

                rlib = invalid
                if len(items) > 7:
                    rlib = os.path.basename(items[7])[3:-6]

                if name in res:
                    for elem in res[name]:
                        if res[name][elem] == size:
                            if elem == invalid:
                                del res[name][elem]
                                res[name] = { rlib: size }
                        else:
                            res[name] = { rlib: size }
                else:
                    res[name] = { rlib: size }

    print outfile
    target = open(outfile, 'w')
    for obj in res:
        rlib = res[obj].keys()[0]
        name = ""
        if rlib != invalid:
            name = rlib + "_"
        name += obj
        target.write(name + ", " + res[obj][rlib] + "\n")
    target.close()
