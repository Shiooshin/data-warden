/* create database */
SELECT 'CREATE DATABASE repositories' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'repositories')\gexec

/* create tables */
CREATE TABLE IF NOT EXISTS repository (
    repo_id SERIAL PRIMARY KEY,
    name VARCHAR ( 50 ) NOT NULL,
    owner VARCHAR ( 50 ) NOT NULL,
    tags VARCHAR ( 256 ) NOT NULL
);

CREATE TABLE IF NOT EXISTS repo_statistics (
    stas_id SERIAL,
    repo_id INT,
    agg_date DATE NOT NULL,
    star_count INT NOT NULL,
    watcher_count INT NOT NULL,
    fork_count INT NOT NULL,
    open_issues INT NOT NULL,
    contributors INT NOT NULL,
    commits INT NOT NULL,
    tags INT NOT NULL,
    closed_issues INT NOT NULL,
    PRIMARY KEY (repo_id, agg_date),
    FOREIGN KEY (repo_id)
        REFERENCES repository (repo_id)
);