Question: 
Would an API that directly queries the MySQL DradisDB to power client-side views like Jobs List, Candidate List, Candidate View be performant at Indeed scale?

Size
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

CREATE DATABASE dradisdb;
USE dradisdb;

DROP TABLE IF EXISTS employer;
CREATE TABLE employer (
    employer_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200)    
);

DROP TABLE IF EXISTS job;
CREATE TABLE job (
    job_id INT(11) UNSIGNED AUTO_INCREMENT,
    employer_id INT(10) UNSIGNED,
    status CHAR(6),
    name VARCHAR(200),
    INDEX (job_id),
    INDEX (employer_id),
    INDEX (status),
    PRIMARY KEY(job_id, employer_id)
);

ALTER TABLE job
    PARTITION BY KEY(employer_id)
    PARTITIONS 10;


DROP TABLE IF EXISTS application;
CREATE TABLE application (
    application_id INT(12) UNSIGNED AUTO_INCREMENT,
    job_id INT(11) UNSIGNED,
    name VARCHAR(200),
    explainer_score INT(4) UNSIGNED,
    sq_score INT(4) UNSIGNED,
    created_at DATE,
    INDEX (application_id), 
    INDEX (job_id), 
    INDEX (name), 
    INDEX (explainer_score), 
    INDEX (sq_score), 
    INDEX (created_at) ,
    PRIMARY KEY(application_id, job_id)
);

ALTER TABLE application ADD INDEX (job_id, application_id);
ALTER TABLE application ADD INDEX (job_id, name);
ALTER TABLE application ADD INDEX (job_id, explainer_score);
ALTER TABLE application ADD INDEX (job_id, sq_score);
ALTER TABLE application ADD INDEX (job_id, created_at);
ALTER TABLE application ADD INDEX (job_id,  created_at, explainer_score, sq_score);


ALTER TABLE application
    PARTITION BY KEY(job_id)
    PARTITIONS 1000;

quit;
```

