#!/bin/bash

#######################
#
i_size=1000
max_delete_queries=10
sleep_interval=15
min_operations=8
max_query_time=1000

USER="user"
PASS="super_secret_password"

log_max_size=1000000
log_file="/var/tmp/clean_up.log"
#
#######################

touch $log_file
log_file_size=`stat -c%s "$log_file"`
if (( $log_file_size > $log_max_size ))
then
    rm -f "$log_file"
fi

delete_queries=`mysql -u user -p$PASS -e  "SELECT * FROM information_schema.processlist WHERE Command = 'Query' AND INFO LIKE 'DELETE FROM big.table WHERE result_timestamp %';"| grep Query|wc -l`

## -- here the hanging DELETE queries will be stopped
mysql-u $USER -p$PASS -e "SELECT ID FROM information_schema.processlist WHERE Command = 'Query' AND INFO LIKE 'DELETE FROM big.table WHERE result_timestamp %'and TIME>$max_query_time;" |grep -v ID| while read -r id ; do
    echo "delete query stopped on `date`" >>  $log_file
    mysql -u $USER -p$PASS -e "KILL $id;"
done

if (( $delete_queries > $max_delete_queries ))
then
  sleep $sleep_interval

  delete_queries=`mysql-u $USER -p$PASS -e  "SELECT * FROM information_schema.processlist WHERE Command = 'Query' AND INFO LIKE 'DELETE FROM big.table WHERE result_timestamp %';"| grep Query|wc -l`

  if (( $delete_queries > $max_delete_queries ))
  then

      sleep $sleep_interval

      delete_queries=`mysql -u $USER -p$PASS -e  "SELECT * FROM information_schema.processlist WHERE Command = 'Query' AND INFO LIKE 'DELETE FROM big.table WHERE result_timestamp %';"| grep Query|wc -l`

      # -- if there are too many delete queries after the second wait
      #  the table will be cleaned up by the next cron job
      if (( $delete_queries > $max_delete_queries ))
        then
            echo "clean-up skipped on `date`" >> $log_file
            exit 1
        fi
  fi

fi

running_operations=`mysql-u $USER -p$PASS -p -e "SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST WHERE COMMAND != 'Sleep';"| wc -l`

if (( $running_operations < $min_operations ))
then
    # -- if the database is not too busy this bigger batch can be processed
    batch_size=$(($i_size * 5))
else
    batch_size=$i_size
fi

echo "starting clean-up on `date`" >>  $log_file

mysql-u $USER -p$PASS -e 'DELETE FROM big.table WHERE result_timestamp < UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 31 DAY))*1000 limit '"$batch_size"';'

if [ $? -eq 0 ]; then
    # -- if the sql command exited normally the exit code will be 0
    echo "delete finished successfully on `date`" >>  $log_file
else
    echo "delete failed on `date`" >>  $log_file
fi