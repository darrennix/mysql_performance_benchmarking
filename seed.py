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
	table = input("\n\n\nWhich table do you want to seed (advertiser, job, candidate): ")
	if table not in ["advertiser", "job", "candidate"]:
		print("Invalid input")
		exit()
	print(table)

	limit = input("How many records to insert (expect 20 seconds per 100K): ")
	if limit != "":
		limit = int(limit)
	else:
		limit = 10000
	print(limit)

	if table in ["job", "candidate"]:
		advertiser_id = input("Do you want to insert for one advertiser_id (can be blank): ")
		if advertiser_id != "":
			advertiser_id = int(advertiser_id)
		else:
			advertiser_id = None
		print(advertiser_id)

	if table in ["candidate"]:
		ats_job_id = input("Do you want to insert for one ats_job_id (can be blank): ")
		if ats_job_id != "":
			ats_job_id = int(ats_job_id)
		else:
			ats_job_id = None
		print(ats_job_id)


	start_time = time.time()

	if(table == "advertiser"):
		advertiser(limit)
	elif(table == "job"):
		job(advertiser_id, limit)
	elif(table == "candidate"):
		candidate(advertiser_id, ats_job_id, limit)

	print("--- %s seconds ---" % (time.time() - start_time))


def advertiser(limit):
	fake = Faker()
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	sql = """
			INSERT INTO tblATS_advertiser (company, advertiser_number) VALUES (%s, %s)
	   """

	values = []
	for i in range(0, limit):
		values.append((fake.company(), random.randrange(100000)))

	cursor.executemany(sql, values)
	db.commit()
	db.close()



def job(advertiser_id, limit):
	fake = Faker()
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()


	if advertiser_id:
		advertiser_ids = [advertiser_id]
	else:
		sql = "SELECT advertiser_id FROM tblATS_advertiser ORDER BY RAND() LIMIT " + str(int(math.ceil(limit / 10)))	
		cursor.execute(sql)		
		data = cursor.fetchall()
		advertiser_ids = [item for t in data for item in t] 

	# Build an autoincrementer for ats_job_id
	autoincrement = {}
	for advertiser_id in advertiser_ids:
		autoincrement[advertiser_id] = 0

	# Update the values if jobs already exist
	advertiser_ids_string = ", ".join([str(integer) for integer in advertiser_ids])
	sql = "SELECT advertiser_id, max(ats_job_id) FROM tblATS_job WHERE advertiser_id IN (" + advertiser_ids_string + ") group by advertiser_id"
	cursor.execute(sql)		
	data = cursor.fetchall()

	for row in data:
		autoincrement[row[0]] = row[1]


	sql = """
			INSERT INTO tblATS_job 
			(advertiser_id, ats_job_id, job_group_id, title, company, country, description, status, account_id) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
	   """

	values = []
	for i in range(0, limit):
		advertiser_id = random.choice(advertiser_ids)
		autoincrement[advertiser_id] = autoincrement[advertiser_id] + 1
		ats_job_id = autoincrement[advertiser_id]
		row = (advertiser_id, ats_job_id, random.randrange(1000000), fake.job(), fake.company(), random.choice(['US', 'CA', 'GB']), "lorem ipsum", random.choice(['ACTIVE', 'PAUSED', 'DELETED']), random.randrange(1000000))
		values.append(row)

	cursor.executemany(sql, values)
	db.commit()
	db.close()



def candidate(advertiser_id, ats_job_id, limit):
	fake = Faker()
	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	if advertiser_id and ats_job_id:
		sql = "SELECT advertiser_id, ats_job_id FROM tblATS_job WHERE advertiser_id = %s and ats_job_id = %s"
		cursor.execute(sql, [advertiser_id, ats_job_id])		
		jobs = cursor.fetchall()
	else:
		sql = "SELECT advertiser_id, ats_job_id FROM tblATS_job ORDER BY RAND() LIMIT " + str(int(math.ceil(limit / 100)))	
		cursor.execute(sql)		
		jobs = cursor.fetchall()


	# Build an autoincrementer for candidate_id
	autoincrement = {}
	for row in jobs:
		advertiser_id = row[0]
		ats_job_id = row[1]
		key = "-".join([str(advertiser_id), str(ats_job_id)])
		autoincrement[key] = 0

		sql = "SELECT max(candidate_id) FROM tblATS_job_candidate WHERE advertiser_id = %s AND ats_job_id = %s"
		cursor.execute(sql, [advertiser_id, ats_job_id])		
		data = cursor.fetchone()
		if data[0]:
			autoincrement[key] = data[0]


	sql = """
		INSERT INTO tblATS_job_candidate 
		(advertiser_id, ats_job_id, candidate_id, source, name, last_job_title, explainer_score, screener_question_score, date_created) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
	"""


	values = []
	for i in range(0, limit):
		row = random.choice(jobs)
		advertiser_id = row[0]
		ats_job_id = row[1]
		date_created = datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), 2020), '%j %Y').isoformat()

		key = "-".join([str(advertiser_id), str(ats_job_id)])

		autoincrement[key] = autoincrement[key] + 1
		candidate_id = autoincrement[key]

		source = random.choice(['MANUAL','RESUME_IMPORT','LINKED_IN_IMPORT','INDEED_APPLY'])
		row = (advertiser_id, ats_job_id, candidate_id, source, fake.name(), fake.job(), random.randrange(3000), random.randrange(99), date_created)
		values.append(row)

	cursor.executemany(sql, values)
	db.commit()
	db.close()


if __name__ == "__main__":
	start()
