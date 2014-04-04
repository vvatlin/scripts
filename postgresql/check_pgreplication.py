#!/usr/bin/env python
# Writen by Vadim Vatlin <vvvvatlin@gmail.com>
# Description:
#	Calculate lag between master and standby servers.
#
#	Use select pg_current_xlog_location() on master and 
#	select pg_last_xlog_replay_location() to get current 
#	wal segment position.
#	
#	Setup:
#		RPM based: yum install python-psycopg2

import sys, getopt
import psycopg2

# global variables
db_name = 'postgres'
MASTER_TYPE="MASTER"
STANDBY_TYPE="STANDBY"

def get_wal_pos(hostname, user, passwd, type):
	conn = psycopg2.connect(database=db_name, user=user, password=passwd, host=hostname)
	cur = conn.cursor()

	if type == MASTER_TYPE:
		cur.execute("select pg_current_xlog_location()")
	elif type == STANDBY_TYPE:
		cur.execute("select pg_last_xlog_replay_location()")
	else:
		return -1

	wal_position = cur.fetchone()[0]

	cur.close()
	conn.close()

	return wal_position

def get_wal_segment_size(hostname, user, passwd):
        conn = psycopg2.connect(database=db_name, user=user, password=passwd, host=hostname)
	cur = conn.cursor()

	cur.execute("show wal_segment_size")
	segment_size = cur.fetchone()[0]

	cur.close()
	conn.close()

	return segment_size

def main(argv):
	master_ip = None
	standby_ip = None
	master_user = None
	master_passwd = None
	standby_user = None  
	standby_passwd = None

	try:
		opts, args = getopt.getopt(argv,'',['master_ip=', 'master_user=','master_passwd=',\
						'standby_ip=', 'standby_user=', 'standby_passwd=',\
						'help'])
	except getopt.GetoptError:
		print ''
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--help':
			print 'check_pgreplication.py \n\
			--master_ip=<master ip-address> \n\
			--master_user=<username> \n\
			--master_passwd=<password> \n\
			--standby_ip=<standby ip-address> \n\
			--standby_user=<username> \n\
			--standby_passwd=<password>'
			print 'standby username and password can be omitted if it is the same as master username and password'
			sys.exit()
		elif opt in ("--master_ip="):
			master_ip = arg
		elif opt in ("--standby_ip="):
			standby_ip = arg
		elif opt in ("--master_user="):
			master_user = arg
		elif opt in ("--master_passwd="):
			master_passwd = arg
		elif opt in ("--standby_user="):
			standby_user = arg
		elif opt in ("--standby_passwd="):
			standby_passwd = arg

		if (standby_user is None) or (standby_passwd is None):
			standby_user = master_user
			standby_passwd = master_passwd

	# get WAL file position on master and stadby
	m_segment, m_segment_offset = get_wal_pos(master_ip, master_user, master_passwd, MASTER_TYPE).split('/')
	s_segment, s_segment_offset = get_wal_pos(standby_ip, standby_user, standby_passwd, STANDBY_TYPE).split('/')

	# get wal segment size, usually 16M
	segment_size = get_wal_segment_size(master_ip, master_user, master_passwd)[:-2]

	# calculate lag in megabytes
	lag = (int(m_segment,16) - int(s_segment,16)) * int(segment_size) + (int(m_segment_offset,16) - int(s_segment_offset,16)).__abs__() / 1024 / 1024

	print lag

if __name__ == "__main__":
	main(sys.argv[1:])
