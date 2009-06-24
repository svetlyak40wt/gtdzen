CREATE TABLE tags_new (
    id INTEGER NOT NULL,
    title VARCHAR(40) NOT NULL,
    PRIMARY KEY (id),
     UNIQUE (title)
);
CREATE TABLE tasks_new (
    id INTEGER NOT NULL,
    title VARCHAR(40) NOT NULL,
    note TEXT,
    priority FLOAT NOT NULL,
    done BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO tags_new SELECT * FROM tags;
INSERT INTO tasks_new SELECT * FROM tasks;

DROP TABLE tags;
ALTER TABLE tags_new RENAME TO tags;
DROP TABLE tasks;
ALTER TABLE tasks_new RENAME TO tasks;
