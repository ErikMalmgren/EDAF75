DROP TABLE IF EXISTS colleges;
CREATE TABLE colleges (
  c_name       TEXT,
  state        TEXT,
  enrollment   INT,
  PRIMARY KEY  (c_name, state)
);

DROP TABLE IF EXISTS students;
CREATE TABLE students (
  s_id         INTEGER,
  s_name       TEXT,
  gpa          REAL,
  size_hs      INT,
  PRIMARY KEY  (s_id)
);

DROP TABLE IF EXISTS applications;
CREATE TABLE applications (
  s_id         INTEGER,
  c_name       TEXT,
  major        TEXT,
  decision     TEXT,
  PRIMARY KEY  (s_id, c_name, major),
  FOREIGN KEY  (s_id) REFERENCES students(s_id),
  FOREIGN KEY  (c_name) REFERENCES colleges(c_name)
);
