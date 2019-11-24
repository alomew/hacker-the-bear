from makerecord import *
from dbclass import Database

timedata = data1[0:5]
username = data1[5]

d = Database()
output = d.analysis(timedata, username)
print(output)