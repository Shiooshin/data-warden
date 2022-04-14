/* create database */
SELECT 'CREATE DATABASE repositories' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'repositories')\gexec

/* create tables */
CREATE TABLE IF NOT EXISTS repository (
    name VARCHAR ( 50 ) NOT NULL PRIMARY KEY,
    owner VARCHAR ( 50 ) NOT NULL,
    tags VARCHAR ( 256 ) NOT NULL
);

CREATE TABLE IF NOT EXISTS repo_statistics (
    stas_id SERIAL,
    repo_name VARCHAR ( 50 ) NOT NULL,
    agg_date DATE NOT NULL,
    star_count INT NOT NULL,
    watcher_count INT NOT NULL,
    fork_count INT NOT NULL,
    open_issues INT NOT NULL,
    contributors INT NOT NULL,
    commits INT NOT NULL,
    closed_issues INT NOT NULL,
    PRIMARY KEY (repo_name, agg_date),
    FOREIGN KEY (repo_name)
        REFERENCES repository (name)
);

CREATE TYPE StatusEnum AS ENUM('SUCCESS','RUNNING','ERROR', 'NA');

CREATE TABLE IF NOT EXISTS etl_status (
    agg_date DATE NOT NULL,
    status StatusEnum NOT NULL DEFAULT 'NA',
    PRIMARY KEY (agg_date)
);