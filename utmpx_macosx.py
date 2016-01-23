import struct, time, sys
from time import strftime
import os
import argparse
from ctypes import *
from tableprint import columnprint

#PAGESIZE = 628

class _UTMPX(LittleEndianStructure):
	_UTX_USERSIZE = 256
	_UTX_IDSIZE = 4
	_UTX_LINESIZE = 32
	_UTX_HOSTSIZE = 256
	_fields_ = [
		("ut_user", c_char*_UTX_USERSIZE),
		("ut_id", c_char*_UTX_IDSIZE),
		("ut_line", c_char*_UTX_LINESIZE),
		("ut_pid", c_int),
		("ut_type", c_short),
		("unknown", c_short),
		("ut_sec", c_int),
		("ut_usec", c_int),
		("ut_host", c_char*_UTX_HOSTSIZE),
		("ut_pad", c_int*16)
	]


def _memcpy(buf, fmt):
	return cast(c_char_p(buf), POINTER(fmt)).contents

ut_type = ["UT_UNKNOWN", "RUN_LVL", "BOOT_TIME", "NEW_TIME", "OLD_TIME", "INIT_PROCESS", "LOGIN_PROCESS", "USER_PROCESS", "DEAD_PROCESS", "ACCOUNTING", "HEADER"]

def who(utmpfile):
	f = open(utmpfile,"rb")
	fsize = os.fstat(f.fileno()).st_size
	buf   = f.read()
	f.close()
	#cut     = lambda s: str(s).split("\0",1)[0]
	out     = []

	for offset in xrange(sizeof(_UTMPX), fsize, sizeof(_UTMPX)):
		out.append(_memcpy(buf[offset:offset+sizeof(_UTMPX)], _UTMPX))

	return out

def main():
	parser = argparse.ArgumentParser(description='utmpx Parser by @n0fate.')
	parser.add_argument('-f', '--file', nargs=1, help='utmpx file(/var/run/utmpx)', required=True)
	args = parser.parse_args()

	strtype = ''
	headerlist = ["user", "session", "terminal", "pid", "start time(utc+0)", "status", "ip", ""]
	contentlist = []
	entries = who(args.file[0])
	for _utmpx in entries:
		if ut_type[int(_utmpx.ut_type)] == 'BOOT_TIME':
			_utmpx.ut_user = 'reboot'
			_utmpx.ut_id = '~'
			strtype = '~'
		elif ut_type[int(_utmpx.ut_type)] == 'USER_PROCESS':
			strtype = 'still logged in'
		lotime = strftime("%a %b %d %H:%M:%S",time.gmtime(float(_utmpx.ut_sec)))
		line = ['%s'%_utmpx.ut_user]
		line.append('%s'%_utmpx.ut_id)
		line.append('%s'%_utmpx.ut_line)
		line.append('%d'%int(_utmpx.ut_pid))
		line.append('%s.%03d'%(lotime, int(_utmpx.ut_usec)/1000))
		line.append('%s'%strtype)
		line.append('%s'%_utmpx.ut_host)
		line.append('')
		contentlist.append(line)

	mszlist = [-1, -1, -1, -1, -1, -1, -1, -1]
	columnprint(headerlist, contentlist, mszlist)

if __name__ == "__main__":
	main()
#EOF
