#!/bin/env python
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

import psycopg2

# variables
# TODO: use getopt module
db_name = 'postgres'
db_user = 'set db user'
db_pass = 'set db password'

master = 'set master server ip or fqdn'
standby = 'set master server ip or fqdn'

# in megabytes
lag_alert = '1'

def get_wal_pos(hostname, type):
	conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=hostname)
	cur = conn.cursor()

	if type == 'master':
		cur.execute("select pg_current_xlog_location()")
	elif type == 'standby':
		cur.execute("select pg_last_xlog_replay_location()")
	else:
		return -1
	wal_pos = cur.fetchone()[0]

	cur.close()
	conn.close()

	return wal_pos

def get_wal_seg_size(hostname):
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=hostname)
	cur = conn.cursor()

	cur.execute("show wal_segment_size")
	segment_size = cur.fetchone()[0]

	cur.close()
	conn.close()

	return segment_size

# get wal position
m_segment, m_segment_offset = get_wal_pos(master, 'master').split('/')
s_segment, s_segment_offset = get_wal_pos(standby, 'standby').split('/')

# get wal segment size, usually 16M
segment_size = get_wal_seg_size(master)[:-2]

# calculate lag in megabytes
print (int(m_segment,16) - int(s_segment,16)) * int(segment_size) + (int(m_segment_offset,16) - int(s_segment_offset,16)).__abs__() / 1024 / 1024
