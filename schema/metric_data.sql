CREATE TABLE metric_data (
    repo CHAR(255) NOT NULL,
    sha CHAR(40) NOT NULL,
    metric_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    running_value INTEGER NOT NULL,
    PRIMARY KEY (repo, sha, metric_id)
);
