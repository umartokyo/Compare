DROP TABLE IF EXISTS Comparisons;
DROP TABLE IF EXISTS Objects;
DROP TABLE IF EXISTS History;

CREATE TABLE Comparisons (
    id INTEGER PRIMARY KEY,
    title TEXT
);

CREATE TABLE Objects (
    id INTEGER PRIMARY KEY,
    title TEXT,
    score INTEGER,
    comparison_id INTEGER,
    FOREIGN KEY(comparison_id) REFERENCES Comparisons(id)
);

CREATE TABLE History (
    id INTEGER PRIMARY KEY,
    object1_id INTEGER,
    object2_id INTEGER,
    did_object1_win BOOLEAN,
    comparison_id INTEGER,
    FOREIGN KEY(comparison_id) REFERENCES Comparisons(id),
    FOREIGN KEY(object1_id) REFERENCES Objects(id),
    FOREIGN KEY(object2_id) REFERENCES Objects(id)
);