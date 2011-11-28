#!/bin/bash

/usr/bin/mysqlcheck -A &>/dev/null

for db in `/usr/bin/mysql -N -e 'show databases' | grep -vE 'mysql|Database|information_schema'`; do

        for table in `/usr/bin/mysql -N -e "use $db; show table status" | grep 'is marked as crashed' | awk '{print $1}'`; do
                echo $db $table;
                /usr/bin/mysqlcheck -rm $db $table
        done
done
