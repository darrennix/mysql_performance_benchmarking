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


	print("\n\n--- Start timer")
	start_time = time.time()
	print("No sort, limit 50")
	cursor.execute("""
		SELECT
			*
		FROM 
			tblATS_job_candidate
		WHERE
			advertiser_id = 1 
			AND ats_job_id = 1
		LIMIT
			50
		""", )
	data = cursor.fetchall()
	print("--- %s seconds ---" % (time.time() - start_time))


	print("\n\n--- Start timer")
	start_time = time.time()
	print("Sort by candidate_id (substitute for created_date), limit 50")
	cursor.execute("""
		SELECT
			*
		FROM 
			tblATS_job_candidate
		WHERE
			advertiser_id = 1 
			AND ats_job_id = 1
		ORDER BY
			candidate_id ASC
		LIMIT
			50
		""", )
	data = cursor.fetchall()
	print("--- %s seconds ---" % (time.time() - start_time))





	print("\n\n--- Start timer")
	start_time = time.time()
	print("Sort by explainer_score, limit 50")
	cursor.execute("""
		SELECT
			*
		FROM 
			tblATS_job_candidate
		WHERE
			advertiser_id = 1 
			AND ats_job_id = 1
		ORDER BY
			explainer_score ASC
		LIMIT
			50
		""", )
	data = cursor.fetchall()
	print("--- %s seconds ---" % (time.time() - start_time))



	print("\n\n--- Start timer")
	start_time = time.time()
	print("Sort by name, limit 50")
	cursor.execute("""
		SELECT
			*
		FROM 
			tblATS_job_candidate
		WHERE
			advertiser_id = 1 
			AND ats_job_id = 1
		ORDER BY
			name ASC
		LIMIT
			50
		""", )
	data = cursor.fetchall()
	print("--- %s seconds ---" % (time.time() - start_time))



	print("\n\n--- Start timer")
	print("Multicolumn sort by created_at, explainer_score WHERE screener_question_score > 10 and explainer_score < 1000, limit 50")
	sql = """
		SELECT
			*
		FROM 
			tblATS_job_candidate
		WHERE
			advertiser_id = 1 
			AND ats_job_id = 1
			and screener_question_score > 10
			and explainer_score < 1000
		ORDER BY
			candidate_id, explainer_score
		LIMIT
			50
		"""
	print(sql)
	start_time = time.time()
	cursor.execute(sql, )
	data = cursor.fetchall()
	print("--- %s seconds ---" % (time.time() - start_time))



	print("\n\n--- Start timer")
	print("Sort by name across all jobs on advertiser, limit 50")
	sql = """
		SELECT
			*
		FROM 
			tblATS_job_candidate
		WHERE
			advertiser_id = 1 
		ORDER BY
			name
		LIMIT
			50
		"""
	print(sql)
	start_time = time.time()
	cursor.execute(sql, )
	data = cursor.fetchall()
	print("--- %s seconds ---" % (time.time() - start_time))


	db = pymysql.connect("localhost","root","","dradisdb" )
	cursor = db.cursor()

	cursor.execute("SELECT count(*)  FROM tblATS_advertiser")
	data = cursor.fetchone()
	print("tblATS_advertiser rows: ", data)


	cursor.execute("SELECT count(*)  FROM tblATS_job")
	data = cursor.fetchone()
	print("tblATS_job rows: ", data)

	cursor.execute("SELECT count(*) FROM tblATS_job_candidate")
	data = cursor.fetchone()
	print("tblATS_job_candidate rows: ", data)


	cursor.execute("SELECT count(*)  FROM tblATS_job WHERE advertiser_id = 1")
	data = cursor.fetchone()
	print("Jobs for advertiser_id = 1: ", data)

	cursor.execute("SELECT count(*) FROM tblATS_job_candidate WHERE advertiser_id = 1 and ats_job_id = 1")
	data = cursor.fetchone()
	print("tblATS_job_candidates for advertiser_id = 1 and ats_job_id = 1 ", data)

	# disconnect from server
	db.close()

if __name__ == "__main__":
	start()
