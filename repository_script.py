import requests
import re
from sets import Set
import os
#print users
f = open('repository.csv', 'w')
with open('users.txt') as file:
    for line in file:
        url = 'http://api.github.com/users/{}/repos'.format(line.rstrip())
        r = requests.get(url, auth=(os.environ['github_user'], os.environ['github_pass']))
        if r.status_code == 200:
            content = r.json()
            tot_commits = 0
            language_count = 0
            languages = Set([])
            for row in content:
                req = requests.get(row['commits_url'][:row['commits_url'].find('{')], auth=(os.environ['github_user'], os.environ['github_pass']))
                language = row['language']
                tot_commits += len(req.json())
                if language is not None:
                    if language not in languages:
                        language_count += 1
                        languages.add(language)
            print >> f, line.rstrip() + "," + str(tot_commits) + "," + str(language_count) 
            
f.close 
