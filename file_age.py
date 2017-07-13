import time, os, subprocess, sys, traceback
from datetime import datetime
from date_diff import date_dif_precomputed
from parse_date_str import parse_date_str

"""
This module contains functions that return file's age on
different OS.
"""

def get_file_age_default(path, cur_parsed, cur_datetime):
	"""
	default function works on mosts OS. It uses mtime timestamp because
	alot of UNIX like OS do not provide crtime timestamp.
	"""
	mtime = datetime.fromtimestamp(os.path.getmtime(path))
	mtime = str(mtime).split(' ')[0]
	mtime = parse_date_str(mtime, '-', 0, 1, 2)
	print("file mtime: {}".format(mtime))
	date_dif = date_dif_precomputed(cur_parsed[0], cur_parsed[1], cur_parsed[2], mtime[0], mtime[1], mtime[2])
	return date_dif

def get_file_age_linux(path, cur_parsed, cur_datetime):
	"""
	This function tryes to get crtime on Linux OS if it is available (ext4 fs and some other fs)
	if it fails to retrive crtime timestamp (if fs do not keep it) then it falls back to
	default function.
	"""
	try:
		# calls standard stat command to get file's inode
		inode = subprocess.check_output(["stat", "-c", "%i", path])
		print("inode: " + inode)
		inode = int(inode)
		# calls df command to get fs type
		fs = subprocess.check_output(["df", "--output=source", path])
		print("fs: " + fs)
		fs = str(fs).split("\n")[1]
		# calls debugfs in order to get crtime timesamp
		crtime_str = os.popen("sudo debugfs -R 'stat <"+str(inode)+">' "+fs+" | grep -E 'crtime'").read()
		print("crtime: "+crtime_str)
		crtime_str = crtime_str.split(" -- ")[1]
		crtime = parse_date_str(crtime_str, ' ', 4, 1, 2)
		print("file crtime: {}".format(crtime))
		date_dif = date_dif_precomputed(cur_parsed[0], cur_parsed[1], cur_parsed[2], crtime[0], crtime[1], crtime[2])
		return date_dif
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		print("EXCEPTION! fallback to mtime!")
		traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
		return get_file_age_default(path, cur_parsed, cur_datetime)

def get_file_age_win(path, cur_parsed, cur_datetime):
	""" this function gets crtime timestamp on Windows OS """
	try:
		date_str = time.ctime(os.path.getctime(path))
		date_parsed = parse_date_str(date_str, ' ', 4, 1, 2)
		print("file crtime: {}".format(date_parsed))
		date_dif = date_dif_precomputed(cur_parsed[0], cur_parsed[1], cur_parsed[2], date_parsed[0], date_parsed[1], date_parsed[2])
		return date_dif
	except:
		print("EXCEPTION! fallback to mtime!")
		return get_file_age_default(path, cur_parsed, cur_datetime)
