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

ut_type = ["UT_UNKNOWN", "RUN_LVL", "BOOT_TIME", "NEW_TIME", "OLD_TIME", "INIT_PROCESS", "LOGIN_PROCESS", "USER_PROCESS", "DEAD_PROCESS", "ACCOUNTING", "HEADER"]

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
    	data = struct.unpack("32s4s32sih6xiii20x2x16s20x222x",entry)
    	out.append(
    		dict([[name[i],cut(data[i])]
    			for i in range(0,len(data))]))
    return out, dumppage

if len(sys.argv) != 2:
	print >> sys.stderr,'wtmpx parser\t\tMade by @n0fate, Base code : wtmp parser by @ykx100\n\tUsage : python wtmpx.py [wtmpxfile]\n\tExample : python wtmpx.py /var/adm/wtmpx'
	exit(1)

utmpfile = sys.argv[1]

entries = ''

headerlist = ["user", "id","session", "terminal", "pid", "start time(utc+0)", "status", "ip", ""]
contentlist = []
dumppage = []
entries, dumppage = who()

# f = open("output.bin", "wb")

for i in range(0, len(entries)):
	#print int(entries[i]['type'])
	# if ut_type[int(entries[i]['type'])] == 'BOOT_TIME':
	# 	entries[i]['user'] = 'reboot'
	# 	entries[i]['id'] = '~'
	# 	strtype = '~'
	# elif ut_type[int(entries[i]['type'])] == 'USER_PROCESS':
	# 	strtype = 'still logged in'
	# else:
	# 	strtype = ''
	strtype = ''
	lotime = strftime("%a %b %d %H:%M:%S",time.gmtime(float(entries[i]['sec'])))
	#eline = entries[i]['user']+'\t'+entries[i]['id']+'\t'+entries[i]['line']+'\t'+entries[i]['pid']+'\t'+ut_type[int(entries[i]['type'])]+'\t'+lotime+'\t'+entries[i]['usec']+'\t'+entries[i]['ipaddress']
	line = ['%s'%entries[i]['user']]
	line.append('%s'%entries[i]['id'])
	line.append('%s'%entries[i]['session'])
	#line.append('%s'%ut_type[int(entries[i]['type'])])
	line.append('%s'%entries[i]['line'])
	line.append('%d'%int(entries[i]['pid']))
	line.append('%s.%03d'%(lotime, int(entries[i]['usec'])/1000))
	line.append('%s'%strtype)
	line.append('%s(%d)'%(entries[i]['ipaddress'], len(entries[i]['ipaddress'])))
	line.append('')
	contentlist.append(line)

# 	if len(entries[i]['ipaddress']) == 0 and entries[i]['user'] != 'cjones' and entries[i]['user'] != 'skyoo':
# 		f.write(dumppage[i])
# 	if entries[i]['ipaddress'] == '8.80.4.21:0' and entries[i]['user'] != 'cjones' and entries[i]['user'] != 'skyoo':
# 		f.write(dumppage[i])

# f.close()

mszlist = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
columnprint(headerlist, contentlist, mszlist)

#EOF