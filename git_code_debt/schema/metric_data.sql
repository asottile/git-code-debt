CREATE TABLE metric_data (
    sha CHAR(40) NOT NULL,
    metric_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    running_value INTEGER NOT NULL,
    PRIMARY KEY (sha, metric_id)
);

CREATE INDEX metric_data__timestamp_idx ON metric_data (timestamp);
CREATE INDEX metric_data__sha_idx ON metric_data (sha);
