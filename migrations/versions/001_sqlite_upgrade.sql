CREATE TABLE migrate_version (
	repository_id VARCHAR(255) NOT NULL, 
	repository_path TEXT, 
	version INTEGER, 
	PRIMARY KEY (repository_id)
);
CREATE TABLE tags (
	id INTEGER NOT NULL, 
	title VARCHAR(40), 
	PRIMARY KEY (id), 
	 UNIQUE (title)
);
CREATE TABLE tasks (
	id INTEGER NOT NULL, 
	title VARCHAR(40), 
	note TEXT, 
	priority FLOAT, 
	done BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE tasks_tags__tags_tasks (
	tasks_id INTEGER NOT NULL, 
	tags_id INTEGER NOT NULL, 
	PRIMARY KEY (tasks_id, tags_id), 
	 CONSTRAINT tasks_tags_fk FOREIGN KEY(tasks_id) REFERENCES tasks (id), 
	 CONSTRAINT tags_tasks_fk FOREIGN KEY(tags_id) REFERENCES tags (id)
);
