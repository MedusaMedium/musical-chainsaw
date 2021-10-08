#!/usr/bin/env python3
'''
currently only works with nix
- add windows support
'''
import argparse
import os
import subprocess
import sys

DRY_RUN = False
REPLACE_SPACES = False

def cmdln():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--directory",
        type=lambda d:os.path.abspath(d) if os.path.isdir(d) else parser.error("invalid directory"),
        help="directory to extract all zips of. will ignore existing directories in this dir"
    )
    parser.add_argument("--replace_spaces", action="store_true", default=False,
        help="replace spaces in zip file names with underscore"
    )
    parser.add_argument("--dry_run", action="store_true", default=False, 
        help="dont execute commands, just build then print them"
    )
    parser.add_argument("-b","--back_up",
        help="create backup directory before operating"
    )
    return parser.parse_args()

def do_the_unzip(path):
    file_list = subprocess.check_output(["ls","-Al",path])
    # seperate lines and remove 'total #' line
    file_list = file_list.decode().split("\n")[1:]
    # remove empty strings
    file_list = [l for l in file_list if l]
    # remove dirs
    file_list = [l for l in file_list if l[0] != 'd']
    # extract file names
    file_list = [l.split(":")[1].split(" ")[1:] for l in file_list if l]
    # concat files with spaces together
    sep = "\ "
    if REPLACE_SPACES:
        und = "_"
        undscr = [und.join(l) for l in file_list if len(l) != 1]
        spaces = [sep.join(l) for l in file_list if len(l) != 1]
        for s,u in zip(spaces,undscr):
            print(f"mv {os.path.join(path,s)} {os.path.join(path,u)}")
            if not DRY_RUN:
                os.system(f"mv {os.path.join(path,s)} {os.path.join(path,u)}")
        sep = und
    file_list = [sep.join(l) for l in file_list]

    for fname in file_list:
        dirname = fname
        if "\ " in fname:
            dirname = "_".join(dirname.split("\ "))
        dirname = os.path.join(path, dirname.split(".zip")[0])
        fname = os.path.join(path,fname)

        print(f"unzip -q {fname} -d {dirname}")
        if not DRY_RUN:
            os.system(f"unzip -q {fname} -d {dirname}")
        print(f"mv {fname} {dirname}")
        if not DRY_RUN:
            os.system(f"mv {fname} -t {dirname}")
        print()

if __name__ == "__main__":
    args = cmdln()
    DRY_RUN = args.dry_run
    REPLACE_SPACES = args.replace_spaces
    do_the_unzip(args.directory)
