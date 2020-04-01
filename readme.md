Question: 
Would an API that directly queries the MySQL DradisDB to power client-side views like Jobs List, Candidate List, Candidate View be performant at Indeed scale?

Current size of DradisDB (bloodmoon):

select count(*) from tblATS_advertiser; 
31,959,347


select max(ats_job_id) from tblATS_job;
192602

select distinct(advertiser_id) from tblATS_job_candidate_app_info 
where 
    candidate_id > 500000
limit 5

'5947263'
'1523942'
'1652394'
'4136472'
'1880457'



select * from tblATS_advertiser where advertiser_id IN (
'5947263',
'1523942',
'1652394',
'4136472',
'1880457'
)
'5947263','Indeed Hire Master Account','3602220','1284039992712426','2018-04-24 11:12:51','2018-04-24 11:12:51'
'4136472','Loomis Armored US, LLC','4331550','2528037985032732','2018-04-24 11:12:51','2018-04-24 11:12:51'
'1880457','SAS Retail Services','1470598','4129096952254760','2018-04-24 11:12:51','2018-04-24 11:12:51'
'1652394','Hire Dynamics','1336481','5066053678531432','2018-04-24 11:12:51','2018-04-24 11:12:51'
'1523942','Amazon WFS - ITA','1201856','471257877961397','2018-04-24 11:12:51','2020-01-14 18:14:56'


# Hire

select max(ats_job_id) from tblATS_job where advertiser_id IN (
'5947263'
)
124049

select max(candidate_id) from tblATS_job_candidate_app_info where advertiser_id IN (
'5947263'
)
9,380,836



Benchmark DB Size
- Millions of employers
- 10s of millions of jobs
- Billions of applications
- Some jobs have > 1 million applications

Constraints
- Includes ancillary data from Screener Questions, Explainer Score
- Supports pagination
- Supports sorting by: alphabetical name, application date, screener questions score, explainer score
- NOTE: Explicitly should not support search by name, since this search should be powered by ElasticSearch to provide more accurate fuzzy matching.  ElasticSearch returns a list of application IDs, which would then become a query to DradisDB for the application information.

Slowest expected query:
For employer with max jobs, max candidates, sort candidates from all active jobs alphabetically and return 50, offset 500K.

* Steps

** Mac
```
brew install mysql
brew tap homebrew/services
brew services start mysql

pip3 install pymysql
pip3 install faker

mysql -uroot 
```

run create.sql
