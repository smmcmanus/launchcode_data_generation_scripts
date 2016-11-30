import requests
import MySQLdb
import re
import os
db = MySQLdb.connect(host="localhost", port=os.environ['mysql_port'], user=os.environ['mysql_user'], passwd=os.environ['mysql_pass'], db="launchcode_dev")
cursor = db.cursor()
cursor.execute("SELECT github FROM demographics WHERE github IS NOT NULL;")
data =  cursor.fetchall()
user = ""
users = []
for row in data:
    user = row[0].split('/')[len(row[0].split('/'))-1]
    if user != "" and " " not in user and len(user) > 4 and re.match("^[a-zA-Z0-9_]*$", user):
        users.append(user)
    
#print users
f = open('users.csv', 'w')
for user in users:
    url = 'http://api.github.com/users/{}'.format(user) 
    r = requests.get(url, auth=(os.environ['github_user'], os.environ['github_pass']))
    if r.status_code == 200:
        content = r.json()
        url = 'http://api.github.com/users/{}/repos'.format(user)
        req = requests.get(url, auth=(os.environ['github_user'], os.environ['github_pass']))
        followers = row['followers']
        following = row['following']
        number_of_repos = len(req.json())
        print >> f, user + ',' + followers + ',' + following + ',' + number_of_repos
            
f.close 
db.close()
