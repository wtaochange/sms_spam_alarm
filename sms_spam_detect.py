# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText

#interval = "13 hours  50 minutes"
interval = "30 minutes"
interval_count = "20"

textfile = "/usr/pp/ping/a"

import psycopg2
import sys

conn = None
conn_prod = None

#client dictionary list
myarray = {}

# get hacked client list
try:

    sql  = "SELECT "
    sql += "to_did, count(*) "
    sql += "FROM sms_smstransaction "
    sql += "WHERE "
    sql += "created >=now() - interval '%s' " % (interval)
    sql += "GROUP BY to_did "
    sql += "HAVING count(*) > %s " % (interval_count)
    sql += "ORDER BY count(*), to_did "
    print "\n->%s" % (sql)


    conn_string = "host='---' dbname='---' user='---' password='---'"
    print "Connecting to database\n->%s" % (conn_string)

    conn = psycopg2.connect(conn_string)

    cur = conn.cursor()
    cur.execute(sql)
    #ver = cur.fetchone()
    #print ver


    rows = cur.fetchall()
    for row in rows:
        myarray[row[0]] = row[1]

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:
    if conn:
        conn.close()

# check if list is empty
if len(myarray) == 0 :
    print "empty list"
    sys.exit(0)

# email content
f = open(textfile, 'wb')
f.write(" %s \n" % sql)
for key, value in myarray.items():
    f.write("\ncell [%s], count [%s] " % (key, value))
    print "%s %s" % (key, value)
f.close()

# send email
fp = open(textfile, 'rb')
msg = MIMEText(fp.read())
fp.close()

msg['Subject'] = 'Potential SMS Spam Notice (Urgent)'
msg['From'] = "no-reply@xxx.com"
msg['To'] = "support@xxx.com"

s = smtplib.SMTP('localhost')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()


