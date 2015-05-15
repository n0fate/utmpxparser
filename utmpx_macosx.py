import struct, time, sys
from time import strftime

from tableprint import columnprint

PAGESIZE = 628


ut_type = ["UT_UNKNOWN", "RUN_LVL", "BOOT_TIME", "NEW_TIME", "OLD_TIME", "INIT_PROCESS", "LOGIN_PROCESS", "USER_PROCESS", "DEAD_PROCESS", "ACCOUNTING", "HEADER"]

def who():
    f = open(utmpfile,"rb")
    utmpstr    = f.read()
    f.close()
    cut     = lambda s: str(s).split("\0",1)[0]
    name    = ["user", "id", "tty", "pid", "type","sec","usec","ipaddress"]
    out     = []
    for entry in [utmpstr[i:i+PAGESIZE] for i in range(PAGESIZE,len(utmpstr),PAGESIZE)]:
    	data = struct.unpack("256s4s32sih2xii256s64x",entry)
    	out.append(
    		dict([[name[i],cut(data[i])]
    			for i in range(len(data))]))

    return out
        
if len(sys.argv) != 2:
	print >> sys.stderr,'utmpx parser\t\tMade by @n0fate, Base code : utmp parser by @ykx100\n\tUsage : python utmpx.py [utmpxfile]\n\tExample : python utmpx.py /var/run/utmpx'
	exit(1)

utmpfile = sys.argv[1]

entries = ''

headerlist = ["user", "session", "terminal", "pid", "start time(utc+0)", "status", "ip", ""]
contentlist = []
entries = who()
for i in range(0, len(entries)):
	if ut_type[int(entries[i]['type'])] == 'BOOT_TIME':
		entries[i]['user'] = 'reboot'
		entries[i]['id'] = '~'
		strtype = '~'
	elif ut_type[int(entries[i]['type'])] == 'USER_PROCESS':
		strtype = 'still logged in'
	lotime = strftime("%a %b %d %H:%M:%S",time.gmtime(float(entries[i]['sec'])))
	eline = entries[i]['user']+'\t'+entries[i]['id']+'\t'+entries[i]['tty']+'\t'+entries[i]['pid']+'\t'+ut_type[int(entries[i]['type'])]+'\t'+lotime+'\t'+entries[i]['usec']+'\t'+entries[i]['ipaddress']
	line = ['%s'%entries[i]['user']]
	line.append('%s'%entries[i]['id'])
	line.append('%s'%entries[i]['tty'])
	line.append('%d'%int(entries[i]['pid']))
	line.append('%s.%03d'%(lotime, int(entries[i]['usec'])/1000))
	line.append('%s'%strtype)
	line.append('%s'%entries[i]['ipaddress'])
	line.append('')
	contentlist.append(line)

mszlist = [-1, -1, -1, -1, -1, -1, -1, -1]
columnprint(headerlist, contentlist, mszlist)

#EOF
