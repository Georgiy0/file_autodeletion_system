import os, platform, sys, time
from datetime import datetime
from date_diff import date_dif_precomputed
from parse_date_str import parse_date_str
from file_age import get_file_age_win, get_file_age_linux, get_file_age_default

"""
This module is called by scheduler in order to clean files of
specified age in certain directory. The script returns 0 on success
and -1 if an error occured during execution.
"""

def search(path, age):
    """
    Iterates recursively through a dictionary. Computes the age of each
    file and delete it if the file's age exceeds argument age.
    """
    # gets information about the OS in order
    # to set platform dependent functions
    current_platform = platform.system()
    print("Current platform: {}".format(current_platform))
    get_file_age = get_file_age_default
    if current_platform == 'Windows':
        get_file_age = get_file_age_win
    # checks weather the process has superuser privileges
    # which are needed to retrieve crtime from ext4 and some other FS
    if current_platform == 'Linux' and os.geteuid() == 0:
        get_file_age = get_file_age_linux
    # gets current system time
    cur = datetime.now()
    cur_parsed = parse_date_str(str(cur).split(' ')[0], '-', 0, 1, 2)
    print("current time: {}\nparsed: {}".format(cur, cur_parsed))
    # directory walk cycle
    for subdir, dirs, files in os.walk(path):
        for file in files:
            path_to_file = subdir + os.sep + file
            print("current file: {}".format(path_to_file))
            # gets current file age
            file_age = get_file_age(path_to_file, cur_parsed, cur)
            print("file: {}\nfile_age = {}".format(file, file_age))
            if file_age >= age:
                print("DELETING {}".format(file))
                os.remove(path_to_file)
    exit(0)

def main():
    """ Checks commad string arguments and calls search() """
    if len(sys.argv) < 3:
        if len(sys.argv) == 1:
            print("autodel.py is a script that deletes old files in a directory.")
            print("It requires 2 arguments:")
            print("\t1) path to the directory where the files are stored,")
            print("\t2) Age of files to be deleted in days.")
            print("example of use: python autodel.py project/logs 3")
            print("will delete all files that are older than 3 days in project/logs and all its subdirs.")
            exit(-1)
        else:
            print("Not enough arguments!")
            exit(-1)
    # checks weather the directory is valid
    if not os.path.isdir(sys.argv[1]):
        print("Invalid directory path!")
        exit(-1)
    try:
        days = int(sys.argv[2])
    except ValueError:
        print("Invalid file age!")
        exit(-1)
    if days >= 0:
        search(sys.argv[1], days)
    else:
        print("Negative file age!")
        exit(-1)

main()
