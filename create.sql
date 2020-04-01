
CREATE DATABASE dradisdb;
USE dradisdb;


-- 
-- tblATS_advertiser
-- 
DROP TABLE IF EXISTS tblATS_advertiser;
CREATE TABLE `tblATS_advertiser` (
  `advertiser_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `company` varchar(255) NOT NULL,
  `source_id` int(10) unsigned DEFAULT NULL,
  `advertiser_number` char(16) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`advertiser_id`),
  KEY `date_created_idx` (`date_created`),
  KEY `last_modified_idx` (`last_modified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Information about Advertisers.';

ALTER TABLE tblATS_advertiser
    PARTITION BY KEY(advertiser_id)
    PARTITIONS 10;




-- 
-- tblATS_job
-- 
DROP TABLE IF EXISTS tblATS_job;
CREATE TABLE `tblATS_job` (
  `advertiser_id` int(10) unsigned NOT NULL COMMENT 'The advertiser to which this job belongs.',
  `ats_job_id` int(10) unsigned NOT NULL COMMENT 'Unique job ID value for the given advertiser.',
  `job_group_id` int(10) unsigned NOT NULL COMMENT 'Key into tblATS_job_group.',
  `title` varchar(255) NOT NULL,
  `company` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `country` char(2) CHARACTER SET latin1 NOT NULL,
  `language` varchar(5) DEFAULT NULL,
  `description` text NOT NULL,
  `status` enum('ACTIVE','PAUSED','DELETED','ARCHIVED','DRAFT') NOT NULL,
  `job_type` set('FULL','PART','TEMP','INTERN','CONTRACT','NONPROFIT','COMMISSION','TELECOMMUTE','RECRUITER','SPAM','VOLUNTEER','FLYIN_FLYOUT','NEW_GRAD','CASUAL','SUBCONTRACT','PERMANENT','APPRENTICESHIP','CUSTOM_1') DEFAULT NULL,
  `salaryLM1` bigint(20) unsigned DEFAULT NULL COMMENT 'Salary Amount one in minor local currency units',
  `salaryLM2` bigint(20) unsigned DEFAULT NULL COMMENT 'Salary Amount two in minor local currency units',
  `salary_period` enum('HOUR','DAY','MONTH','YEAR','WEEK') DEFAULT NULL,
  `education` enum('COLLEGE') DEFAULT NULL,
  `authorized_to_work` tinyint(1) DEFAULT NULL,
  `account_id` int(10) unsigned NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `views` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'The number of views on the public view job page',
  `view_job_exists` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Indicates if the JASX view job page exists',
  `experience` text,
  `company_info_confidential` tinyint(1) DEFAULT NULL,
  `end_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`advertiser_id`,`ats_job_id`),
  KEY `account_id` (`account_id`),
  KEY `advertiser_id` (`advertiser_id`,`job_group_id`),
  KEY `last_modified` (`last_modified`),
  KEY `idx_date_created` (`date_created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Main job table.';


ALTER TABLE tblATS_job
    PARTITION BY KEY(`advertiser_id`,`ats_job_id`)
    PARTITIONS 100;




-- 
-- tblATS_job_candidate
-- 
DROP TABLE IF EXISTS tblATS_job_candidate;
CREATE TABLE `tblATS_job_candidate` (
  `advertiser_id` int(10) unsigned NOT NULL COMMENT 'The advertiser to which this candidate/job belong.',
  `ats_job_id` int(10) unsigned NOT NULL COMMENT 'Unique job ID value for the given advertiser.',
  `candidate_id` int(10) unsigned NOT NULL COMMENT 'Unique candidate ID for the given advertiser.',
  `source` enum('MANUAL','RESUME_IMPORT','LINKED_IN_IMPORT','INDEED_APPLY','REFERRAL','RESUME_CONTACT','MATCH','INDEED_APPLY_ITA','INVITED','INDEED_APPLY_SPONSORED','JOB_I2A') NOT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT '0',
  `starred` tinyint(1) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `country` char(2) CHARACTER SET latin1 DEFAULT NULL,
  `last_job_title` varchar(255) DEFAULT NULL,
  `last_company` varchar(255) DEFAULT NULL,
  `degree` varchar(255) DEFAULT NULL,
  `field_of_study` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `cover_letter` text,
  `resume_id` int(10) unsigned DEFAULT NULL,
  `ia_app_id` char(24) DEFAULT NULL COMMENT 'IndeepApply reference ID',
  `ia_jobmeta` text,
  `ref_id` int(10) unsigned DEFAULT NULL COMMENT 'tblATS_referral_info key',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NULL DEFAULT NULL,
  `candidate_status_id` int(10) unsigned DEFAULT NULL,
  `rejection_letter_status` enum('NONE','QUEUED','SENT','AUTONOTIFY_PENDING','AUTONOTIFY_CANCELLED','AUTONOTIFY_SENT') NOT NULL,
  `email_hash` bigint(20) DEFAULT NULL COMMENT 'conv(left(md5(trim(lower(email))),16),16,-10); Utilz.get64BitMD5',
  `judy_predict_reviewed` tinyint(1) DEFAULT NULL,
  `judy_predict_hired` tinyint(1) DEFAULT NULL,
  `dremr_email` varchar(255) DEFAULT NULL,
  `row_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`advertiser_id`,`ats_job_id`,`candidate_id`),
  KEY `lmd` (`last_modified`),
  KEY `email_hash` (`email_hash`),
  KEY `row_modified` (`row_modified`),
  KEY `candidate_id` (`candidate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8 COMMENT='temporary key for migration';


ALTER TABLE tblATS_job_candidate
    PARTITION BY KEY(`advertiser_id`,`ats_job_id`)
    PARTITIONS 1000;



ALTER TABLE tblATS_job_candidate
ADD COLUMN  explainer_score int(5),
ADD COLUMN  screener_question_score int(2)
;