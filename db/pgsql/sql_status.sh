#/bin/sh

#===
#= For PostgreSQL upper 8.4 and 9.0
#= 実行中のSQLクエリ一覧をメールで送信するスクリプト （主に負荷が高まったときに実行する用）
#= this script is to mail the current sql queries for monitoring.
#===

addr_from=`hostname`		# from address
addr_to="foo@bar" 			# to address
subject="SQL Status"		# subject


# SQL
sql=$(/usr/local/pgsql/bin/psql -U postgres -c \"SELECT procpid,start,now() - start AS lap,current_query FROM (SELECT backendid,pg_stat_get_backend_pid(S.backendid) AS procpid,pg_stat_get_backend_activity_start(S.backendid) AS start,pg_stat_get_backend_activity(S.backendid) AS current_query FROM (SELECT pg_stat_get_backend_idset() AS backendid) AS S ) AS S WHERE current_query <> '' ORDER BY lap DESC\")


# Mail
body="From: ${addr_from}\nTo: ${addr_to}\nSubject: ${subject}\n\n${sql}"
echo -e "${body}" | /usr/sbin/sendmail -t ${addr_to}
