CREATE TABLE metric_changes (
    sha CHAR(40) NOT NULL,
    metric_id INTEGER NOT NULL,
    value INTEGER NOT NULL,
    PRIMARY KEY (sha, metric_id)
);
