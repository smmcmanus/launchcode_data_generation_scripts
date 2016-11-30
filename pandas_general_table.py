import pandas
import numpy
import MySQLdb
import os
db = MySQLdb.connect(host="localhost", port=os.environ['mysql_port'], user=os.environ['mysql_user'], passwd=os.environ['mysql_pass'], db="launchcode_dev")

cursor = db.cursor();
cursor.execute("select applicants.first_name, applicants.last_name, candidates.status, demographics.birthdate, demographics.gender, demographics.college, demographics.major, demographics.city, demographics.state, demographics.zipcode from applicants left outer join demographics on applicants.id = demographics.applicant_id left outer join candidates on candidates.id = demographics.applicant_id where candidates.status is not null;");

data = cursor.fetchall()
rows = []
for entry in data:
    obj = pandas.Series([entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8], entry[9]])
    rows.append(obj);


frame = pandas.DataFrame(rows)

print frame
