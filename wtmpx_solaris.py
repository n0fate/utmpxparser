import struct, time, sys
from time import strftime

from tableprint import columnprint

PAGESIZE = 372

# struct futmpx {
#         char    ut_user[32];            /* user login name */
#         char    ut_id[4];               /* inittab id */
#         char    ut_line[32];            /* device name (console, lnxx) */
#         pid32_t ut_pid;                 /* process id */
#         int16_t ut_type;                /* type of entry */
#         struct {
#                 int16_t e_termination;  /* process termination status */
#                 int16_t e_exit;         /* process exit status */
#         } ut_exit;                      /* exit status of a process */
#         struct timeval32 ut_tv;         /* time entry was made */
#         int32_t ut_session;             /* session ID, user for windowing */
#         int32_t pad[5];                 /* reserved for future use */
#         int16_t ut_syslen;              /* significant length of ut_host */
#         char    ut_host[257];           /* remote host name */
# };

# https://java.net/projects/solaris/sources/on-src/content/usr/src/head/utmpx.h

ut_type = ["EMPTY", "RUN_LVL", "BOOT_TIME", "OLD_TIME", "NEW_TIME", "INIT_PROCESS", "LOGIN_PROCESS", "USER_PROCESS", "DEAD_PROCESS", "ACCOUNTING", "DOWN_TIME"]

def who():
    dumppage = []
    f = open(utmpfile,"rb")
    utmpstr    = f.read()
    f.close()
    cut     = lambda s: str(s).split("\0",1)[0]
    name    = ["user", "id", "line", "pid", "type","sec","usec","session","ipaddress"]
    out     = []
    for entry in [utmpstr[i:i+PAGESIZE] for i in range(0,len(utmpstr),PAGESIZE)]:
    	dumppage.append(entry)
    	data = struct.unpack(">32s4s32sih6xiii20x2x16s20x222x",entry) # For SPARC System(Big-Endian)
    	out.append(
    		dict([[name[i],cut(data[i])]
    			for i in range(0,len(data))]))
    return out, dumppage

if len(sys.argv) != 2:
	print >> sys.stderr,'wtmpx parser\t\tMade by @n0fate, Base code : wtmp parser by @ykx100\n\tUsage : python wtmpx.py [wtmpxfile]\n\tExample : python wtmpx.py /var/adm/wtmpx'
	exit(1)

utmpfile = sys.argv[1]

entries = ''

headerlist = ["user", "id","session", "type", "terminal", "pid", "start time(utc+0)", "status", "ip", ""]
contentlist = []
dumppage = []
entries, dumppage = who()

# f = open("output.bin", "wb")

for i in range(0, len(entries)):
	iuttype = int(entries[i]['type'])
	
	try:
		if ut_type[iuttype] == 'BOOT_TIME':
			entries[i]['user'] = 'reboot'
			entries[i]['id'] = '~'
			strtype = '~'
		elif ut_type[iuttype] == 'USER_PROCESS':
			strtype = 'still logged in'
		else:
			strtype = ''
	except IndexError:
		strtype = ''
	strtype = ''
	lotime = strftime("%Y %m %d %H:%M:%S",time.gmtime(float(entries[i]['sec'])))
	#eline = entries[i]['user']+'\t'+entries[i]['id']+'\t'+entries[i]['line']+'\t'+entries[i]['pid']+'\t'+ut_type[int(entries[i]['type'])]+'\t'+lotime+'\t'+entries[i]['usec']+'\t'+entries[i]['ipaddress']
	line = ['%s'%entries[i]['user']]
	line.append('%s'%entries[i]['id'])
	line.append('%d'%int(entries[i]['session']))
	try:
		line.append('%s'%ut_type[iuttype])
	except IndexError:
		line.append('')
	line.append('%s'%entries[i]['line'])
	line.append('%d'%int(entries[i]['pid']))
	line.append('%s.%03d'%(lotime, int(entries[i]['usec'])/1000))
	line.append('%s'%strtype)
	line.append('%s'%(entries[i]['ipaddress']))
	line.append('')
	contentlist.append(line)

# 	if len(entries[i]['ipaddress']) == 0 and entries[i]['user'] != 'cjones' and entries[i]['user'] != 'skyoo':
# 		f.write(dumppage[i])
# 	if entries[i]['ipaddress'] == '8.80.4.21:0' and entries[i]['user'] != 'cjones' and entries[i]['user'] != 'skyoo':
# 		f.write(dumppage[i])

# f.close()

mszlist = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
columnprint(headerlist, contentlist, mszlist)

#EOF