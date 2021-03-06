#!/usr/local/bin/python3
# Mark Mariscal, Christopher Piwarski, Wais Robleh
# Midterm Project
# 26 January 2019
# CST363 Databases Online
# this file must be in the /cgi-bin/ directory of the server
from os import environ
import string
import cgitb, cgi
import mysql.connector
cgitb.enable()

form = cgi.FieldStorage()

cookies = environ['HTTP_Cookie']

def find_between(words, first, last):
  try:
    start = words.index(first) + len(first)
    end = words.index(last,start)
    return words[start:end]
  except  ValueError:
    return ""

username = find_between(cookies,"username=",";")
password = find_between(cookies,"password=",";")

# HTML Header
print('Content-Type: text/html')
print()
print('<html><title>CLASSES</title><body>')

try:
    cnx = mysql.connector.connect(user='root',
                                password='root',
                                database='cms',
                                host='127.0.0.1')

    cursor1 = cnx.cursor()
    cursor2 = cnx.cursor()
except mysql.connector.Error as err:
    raise SystemExit
    print("ERROR", err)

student_query = 'SELECT a.user_name, c.class_name, c.classroom_number \
FROM accounts a JOIN classes c ON a.class_id = c.class_id \
WHERE user_name = %s;'

teacher_query = 'SELECT a.user_name, c.class_name, c.classroom_number  \
FROM accounts a JOIN classes c ON a.class_id = c.class_id \
WHERE c.class_id = (SELECT class_id FROM accounts WHERE user_name = %s);'

# determine user level 
ul_query = 'SELECT user_level FROM accounts WHERE user_name = %s'

cursor1.execute(ul_query, (username,))
fetch = cursor1.fetchone()
test = str(fetch)
result = find_between(test,"(",",")

if result == "1":
    print('Here is your class:')
    print('<table border="1"><tr><th>Student Name</th><th>Course</th><th>Room Number</th></tr>')
    cursor2.execute(student_query, (username,))
    classes = cursor2.fetchone()
    print ('<tr><td>%s <td>%s <td>%s </tr>' % classes)
elif result == "2":
    print('Here is your class:')
    print('<table border="1"><tr><th>Course Members</th><th>Course</th><th>Room Number</th></tr>')
    cursor2.execute(teacher_query, (username,))
    classes = cursor2.fetchone()
    while classes is not None:
        print ('<tr><td>%s <td>%s <td>%s </tr>' % classes)
        classes = cursor2.fetchone()
else:
    print('Sorry, you do not have access to view classes')

print('<br>')
print('</table>')
print('<a href="http://127.0.0.1:9000/portal.html">Back Button</a><br/>')
print('</body></html>')
cnx.commit()
cnx.close()
