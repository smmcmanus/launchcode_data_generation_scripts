import requests
import MySQLdb
import urllib
import time
import os
url = "https://api.meaningcloud.com/sentiment-2.1"
key = os.environ['sentiment_key']

db = MySQLdb.connect(host="localhost", port=os.environ['mysql_port'], user=os.environ['mysql_user'], passwd=os.environ['mysql_pass'], db="launchcode_dev")

cursor = db.cursor()
cursor.execute("select candidate_id, learning_journey from experiences where learning_journey is not null and learning_journey != \"\";")
data = cursor.fetchall()
print len(data)
f = open('journey_sentiment.csv', 'w')
print >> f, "candidate_id,sentiment,confidence"

sentiment_dict = {'P+' : 2 , 'P' : 1 ,  'NEU' : 0 , 'N' : -1, 'N+' : -2 , 'NONE' : 0 }
i = 0
for row in data:
    print i
    i += 1
    txt = row[1]
    request = requests.post(url, data={'key' : key, 'txt' : txt, 'lang' : 'en'})
    if request.status_code == 200:
        j = request.json()
        if 'score_tag' not in j or 'confidence' not in j:
            continue
        print >> f,  str(row[0]) + ',' + str(sentiment_dict[j['score_tag']]) + ',' + j['confidence']
    else:
        print request.status_code
    time.sleep(0.5) 
