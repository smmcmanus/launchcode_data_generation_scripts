from __future__ import division
from lxml import html
import requests
import time
import MySQLdb
import os
db = MySQLdb.connect(host="localhost", port=os.environ['mysql_port'], user=os.environ['mysql_user'], passwd=os.environ['mysql_pass'], db="launchcode_dev")
cursor = db.cursor()
cursor.execute("select candidate_id, relevant_project from experiences where relevant_project is not null and relevant_project != \"\";")
data = cursor.fetchall()
print len(data)
url = "http://service.afterthedeadline.com/checkDocument"
f = open('grammar_score_project.csv','w')
print >> f, "candidate_id,relevent_project_analysis,relevant_project_length"
i = 0;
for row in data:
    print i
    why = row[1]
    whyCount = ""
    whyLength = len(why.split())
    if why is None:
        continue
    if whyLength > 5:
        request = requests.post(url, data={'key':os.environ['afterthedeadline_key'], 'data':why})
 	if request.status_code == 200:
            h = html.fromstring(request.content)
            errors = len(h.xpath('error'))
            whyCount = errors / whyLength
        else:
            print "miss"
        time.sleep(0.9)
    
    print >> f, str(row[0]) + "," + str(whyCount) + "," + str(whyLength) 
    i += 1
