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
f = open('repos.csv', 'w')
for user in users:
    url = 'http://api.github.com/users/{}/repos'.format(user)
    r = requests.get(url, auth=(os.environ['github_user'], os.environ['github_pass']))
    if r.status_code == 200:
        content = r.json()
        repo_count = 0
        for row in content:
            repo_count += 1
            req = requests.get(row['commits_url'][:row['commits_url'].find('{')], auth=(os.environ['github_user'], os.environ['github_pass']))
            name = row['name']
            forks = row['forks_count']
            watchers = row['watchers_count']
            language = row['language']
            stars = row['stargazers_count']
            commits = len(req.json())
            if language is None:
                language = "None"
            print >> f, user + ',' + name + ',' + str(forks) + ',' + str(watchers) + ',' + language + ',' + str(stars) + ',' + str(commits)
            if repo_count == 5:
                break
            
f.close 
db.close()
