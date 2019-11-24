from makerecord import *
from dbclass import Database

timedata = data1[0:5]
mooddata = data1[5]
username = data1[6]

d = Database()
output, moodtext = d.analysis(timedata, username)
print(output, moodtext)
