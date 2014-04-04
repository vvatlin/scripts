1. Put check_pgreplication.py to /etc/zabbix/scripts
2. Install psycopg2 python module

3. Write down to zabbix_agentd.conf <br/>
UserParameter=check_pgreplication,/etc/zabbix/scripts/check_pgreplication.py --master_ip=<ip> --standby_ip=<ip> --master_user=<user> --master_passwd=<pass>

4. Write down to master and standby pg_hba.conf <br/>
host    postgres        replmon           0.0.0.0/0               md5

5. Execute such sql statements on master server: <br/>
postgres=# CREATE ROLE replmon NOSUPERUSER LOGIN password 'passW00rd';

6. Import postgresql_template.xml into zabbix.
