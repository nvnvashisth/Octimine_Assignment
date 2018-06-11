#!/usr/bin/python


import os
import pymysql
import xml.etree.ElementTree as ET

"""
Create 3 data member of this class, which will store data from the *.xml

1. PublicationNumber
2. Title
3. Abstract

"""

class Fetched_Data: 
	def __init__(self, Title, PublicationNumber, Abstract):
		self.Title = Title
		self.PublicationNumber = PublicationNumber
		self.Abstract = Abstract
"""
In order to connect the database, change the below parameter accordingly
Hostname -> The place mysql is getting hosted
Username -> Username of mysql 
Password -> Password of mysql
"""

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'nanoDB.db'


"""
Following code will connect to mysql database by using above mentioned parameter and does below following task
1. Create a database by the name of nanoDB
2. Use the database
3. Create the table in which the data going to reside.
"""

myConnection = pymysql.connect(host=hostname, user=username, passwd=password )
cursor = myConnection.cursor()

cursor.execute("create database nanoDB;")
cursor.execute("use nanoDB;")
cursor.execute("create table nanotable(PublicationNumber varchar(15) primary key, Title varchar(2000), Abstract Text);")

#print("Successful connnection")

"""
The below code will parse the each filename present at the following path. The variable 'path' can be modified with location of the *.xml files present. 
Further the code will read the each filename present in the folder where the endoffile name is .xml. Then final output can be 
"""		


path = '/home/nitin/Desktop/nano'

xml_list = []
for filename in os.listdir(path):
	if filename.endswith(".xml"):
		xml_list.append(os.path.join(path,filename)) 


"""
The below for loop will further bring each filename from the above xml_list variable.
Further it will look for the empty situation of Abstract tag. If empty, then it will add a custom string as 'Abstract as empty'
Then the data will be formatted according to need, so that data can be inserted into the table.
"""


for i in xml_list:
	File_Content = ET.parse(i)
	if(File_Content.find('Abstract') is None):
		Abstract = "Abstract is empty"
	else:
		Abstract = File_Content.find('Abstract').text.strip()

	xmlObject = Fetched_Data(File_Content.find('Title').text.strip(),File_Content.find('PublicationNumber').text.strip(),Abstract)
	xmlObject.Abstract = xmlObject.Abstract.replace('"', '\\"')
	xmlObject.Title = xmlObject.Title.replace('"', '\\"')
	values = "(\"" + xmlObject.PublicationNumber + "\",\"" + xmlObject.Title + "\",\"" + xmlObject.Abstract + "\");"
	sql_query = "insert into nanotable values" + values
	cursor.execute(sql_query)

"""
Commit the changes and closing the connection.
"""

myConnection.commit()
myConnection.close()

