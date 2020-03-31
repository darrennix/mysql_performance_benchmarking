#!/usr/bin/python3

import pymysql
import math
import random
import datetime
import time

from faker import Faker
from faker.providers import company
from faker.providers import job


def start():
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	cursor.execute("SELECT count(employer_id)  FROM employer")
	data = cursor.fetchone()
	print("Employer rows: ", data)


	cursor.execute("SELECT count(job_id)  FROM job")
	data = cursor.fetchone()
	print("Job rows: ", data)

	cursor.execute("SELECT count(application_id) FROM application")
	data = cursor.fetchone()
	print("Application rows: ", data)

	start_time = time.time()
	print("--- Start timer")

	cursor.execute("SELECT count(job_id)  FROM job WHERE employer_id = 1")
	data = cursor.fetchone()
	print("Jobs for employer_id = 1: ", data)

	cursor.execute("SELECT count(application_id) FROM job, application WHERE job.employer_id = 1 AND job.job_id = application.job_id")
	data = cursor.fetchone()
	print("Applications for employer_id = 1: ", data)

	print("--- %s seconds ---" % (time.time() - start_time))

	# disconnect from server
	db.close()


	table = input("Which table do you want to seed (employer, job, application): ")
	if table not in ["employer", "job", "application"]:
		print("Invalid input")
		exit()
	print(table)

	parent_id = input("Do you want to seed all records for one employer? Enter employer ID or leave blank: ")
	if parent_id != "":
		parent_id = int(parent_id)
	else:
		parent_id = None
	print(parent_id)

	limit = input("How many records to insert (expect 20 seconds per 100K): ")
	if limit != "":
		limit = int(limit)
	else:
		limit = 10000
	print(limit)


	start_time = time.time()

	if(table == "employer"):
		employer(parent_id, limit)
	elif(table == "job"):
		job(parent_id, limit)
	elif(table == "application"):
		application(parent_id, limit)

	print("--- %s seconds ---" % (time.time() - start_time))


def employer(parent_id, limit):
	fake = Faker()
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	sql = """
			INSERT INTO employer (name) VALUES (%s)
	   """

	values = []
	for i in range(0, limit):
		values.append((fake.company()))

	cursor.executemany(sql, values)
	db.commit()
	db.close()



def job(parent_id, limit):
	fake = Faker()
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	statuses = ['active', 'paused', 'closed']

	if parent_id:
		parent_ids = [parent_id]
	else:
		sql = "SELECT employer_id FROM employer ORDER BY RAND() LIMIT " + str(int(math.ceil(limit / 10)))	
		cursor.execute(sql)		
		data = cursor.fetchall()
		parent_ids = [item for t in data for item in t] 

	sql = """
			INSERT INTO job (employer_id, name, status) VALUES (%s, %s, %s)
	   """

	values = []
	for i in range(0, limit):
		row = (random.choice(parent_ids), fake.job(), random.choice(statuses))
		values.append(row)

	cursor.executemany(sql, values)
	db.commit()
	db.close()



def application(parent_id, limit):
	fake = Faker()
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	if parent_id:
		sql = "SELECT job_id FROM job WHERE employer_id = %s LIMIT 1"
		cursor.execute(sql, parent_id)		
		data = cursor.fetchone()

		parent_ids = [data[0]]
	else:
		sql = "SELECT job_id FROM job ORDER BY RAND() LIMIT " + str(int(math.ceil(limit / 100)))	
		cursor.execute(sql)		
		data = cursor.fetchall()
		parent_ids = [item for t in data for item in t] 

	sql = """
			INSERT INTO application (job_id, name, explainer_score, sq_score, created_at) VALUES (%s, %s, %s, %s, %s)
	   """

	values = []
	for i in range(0, limit):
		date = datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), 2020), '%j %Y').isoformat()
		row = (random.choice(parent_ids), fake.name(), random.randrange(3000), random.randrange(9000), date)
		values.append(row)

	cursor.executemany(sql, values)
	db.commit()
	db.close()



if __name__ == "__main__":
	start()
