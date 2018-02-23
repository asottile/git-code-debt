CREATE TABLE metric_names (
    id INTEGER PRIMARY KEY ASC,
    name CHAR(255) NOT NULL,
    has_data INTEGER DEFAULT 0,
    description BLOB
);
