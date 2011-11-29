#!/bin/sh

#===
#= this is for tranffering n taking backup replication wal files on PostgreSQL (8.4/9.0 higher) system
#===

#=== config ===#
HOST=`hostname`							# for naming each dir name
WAL_DIR='/db_backup'					# wal file directory (local)
KEY_DIR='/home/postgres/.ssh/id_rsa'	# ssh key file (local)
BK_HOST='192.168.0.xxx'					# remote host (incl. user name e.g. postgres@192.168.0.xxx)
BK_DIR='/backup/db_backups/wal_backups'	# backup to this dir (remote)

E_TIME=60								# estimated time to complete rsync


#=== Main Process ===#
rsync -auzv ${WAL_DIR} ${BK_HOST}:${BK_DIR}/${HOST} --rsh='ssh -i ${KEY_DIR}'

if [ $? -eq 0 ];then
  find ${WAL_DIR}/* -type f -mmin +${E_TIME}|xargs rm
fi
