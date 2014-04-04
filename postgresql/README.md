Put check_pgreplication.py to /etc/zabbix/scripts

Write down to zabbix_agentd.conf 
UserParameter=check_pgreplication,/etc/zabbix/scripts/check_pgreplication.py --master_ip=<ip> --standby_ip=<ip> --master_user=<user> --master_passwd=<pass>

Write down to master and standby pg_hba.conf 
host    postgres        clmon           0.0.0.0/0               md5

Execute such sql statements on master server:
postgres=# CREATE ROLE replmon NOSUPERUSER LOGIN password 'passW00rd';

Create item and trigger in zabbix.
