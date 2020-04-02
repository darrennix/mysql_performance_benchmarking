
# Question: 
Would an API that directly queries the MySQL DradisDB to power client-side views like Jobs List, Candidate List, Candidate View be performant at Indeed scale?

### Current size of DradisDB (bloodmoon):

select count(*) from tblATS_advertiser; 
31,959,347


select max(ats_job_id) from tblATS_job;
192,602

####     advertisers with more than 500K candidates:
select * from tblATS_advertiser where advertiser_id IN (
'5947263', # Hire
'1523942',
'1652394',
'4136472',
'1880457'
)


#### Hire

select max(ats_job_id) from tblATS_job where advertiser_id IN (
'5947263'
)
124,049

select max(candidate_id) from tblATS_job_candidate_app_info where advertiser_id IN (
'5947263'
)
9,380,836



# Benchmark 
- Include ancillary data from Screener Questions, Explainer Score
- Support pagination
- Support sorting by: alphabetical name, application date, screener questions score, explainer score
- Support complex filters and sorts e.g. filter on screener question and explainer scores and sort by name
- NOTE: Explicitly should not support search by name, since this search should be powered by ElasticSearch to provide more accurate fuzzy matching.  ElasticSearch returns a list of application IDs, which would then become a query to DradisDB for the application information.

# Installation
```
brew install mysql
brew tap homebrew/services
brew services start mysql

pip3 install pymysql
pip3 install faker
```

### Create Database
Import create.sql
```mysql -uroot ```

### Seed data
Run seed multiple times to create realistic data profile
``` python3 seed.py```

### Benchmark
``` python3 benchmark.py```

# Results

Using the employer with the most jobs (1.1M) and most applications (4.8M): 

- No sort, limit 50
--- 0.01844191551208496 seconds ---


--- Start timer
Sort by candidate_id (substitute for created_date), limit 50
--- 0.00347900390625 seconds ---


--- Start timer
Sort by explainer_score, limit 50
--- 0.010440826416015625 seconds ---


--- Start timer
Sort by name, limit 50
--- 0.012052059173583984 seconds ---


--- Start timer
Multicolumn sort by created_at, explainer_score WHERE screener_question_score > 10 and explainer_score < 1000, limit 50

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
        
--- 0.004594326019287109 seconds ---


--- Start timer
Sort by name across all jobs on advertiser, limit 50

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
        
--- 1.2268850803375244 seconds ---

