import MySQLdb
import re
import requests
import os
db = MySQLdb.connect(host="localhost", port=os.environ['mysql_port'], user=os.environ['mysql_user'], passwd=os.environ['mysql_pass'], db="launchcode_dev")
cursor = db.cursor()
cursor.execute("select demographics.applicant_id, demographics.github, candidate_evaluation_timelines.rejected_date, candidate_evaluation_timelines.benched_date from demographics inner join candidate_evaluation_timelines on demographics.applicant_id = candidate_evaluation_timelines.candidate_id where demographics.github is not null and demographics.is_currently_studying_fulltime is null or demographics.github is not null  and demographics.is_currently_studying_fulltime = 0;")
data = cursor.fetchall()
f = open('github_applicant_ids.csv', 'w')
print >> f, "applicant_id,github_url,github_username,was_successful"
for row in data:
    user = row[1].split('/')[len(row[1].split('/'))-1]
    if user != "" and " " not in user and len(user) > 4 and re.match("^[a-zA-Z0-9]*$", user):
        url = 'http://api.github.com/users/{}'.format(user)
        r = requests.get(url, auth=(os.environ['github_user'], os.environ['github_pass']))
        if r.status_code == 200:
            success = 0
            if row[2] is None and row[3] is None:
                success = 1
            print >> f, str(row[0]) + ',' + row[1] + ',' + user + ',' + str(success)
db.close()    
