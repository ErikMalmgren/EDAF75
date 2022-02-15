DELETE FROM students;
DELETE FROM colleges;
DELETE FROM applications;

INSERT
INTO   students(s_id, s_name, gpa, size_hs)
VALUES (123, 'Amy', 3.9, 1000),
       (234, 'Bob', 3.6, 1500),
       (345, 'Craig', 3.5, 500),
       (456, 'Doris', 3.9, 1000),
       (567, 'Edward', 2.9, 2000),
       (678, 'Fay', 3.8, 200),
       (789, 'Gary', 3.4, 800),
       (987, 'Helen', 3.7, 800),
       (876, 'Irene', 3.9, 400),
       (765, 'Jay', 2.9, 1500),
       (654, 'Amy', 3.9, 1000),
       (543, 'Craig', 3.4, 2000);

INSERT
INTO   colleges(c_name, state, enrollment)
VALUES ('Stanford', 'CA', 15000),
       ('Berkeley', 'CA', 36000),
       ('MIT', 'MA', 10000),
       ('Cornell', 'NY', 21000);
        
INSERT
INTO   applications(s_id, c_name, major, decision)
VALUES (123, 'Stanford', 'CS', 'Y'),
       (123, 'Stanford', 'EE', 'N'),
       (123, 'Berkeley', 'CS', 'Y'),
       (123, 'Cornell', 'EE', 'Y'),
       (234, 'Berkeley', 'biology', 'N'),
       (345, 'MIT', 'bioengineering', 'Y'),
       (345, 'Cornell', 'bioengineering', 'N'),
       (345, 'Cornell', 'CS', 'Y'),
       (345, 'Cornell', 'EE', 'N'),
       (678, 'Stanford', 'history', 'Y'),
       (987, 'Stanford', 'CS', 'Y'),
       (987, 'Berkeley', 'CS', 'Y'),
       (876, 'Stanford', 'CS', 'N'),
       (876, 'MIT', 'biology', 'Y'),
       (876, 'MIT', 'marine biology', 'N'),
       (765, 'Stanford', 'history', 'Y'),
       (765, 'Cornell', 'history', 'N'),
       (765, 'Cornell', 'psychology', 'Y'),
       (543, 'MIT', 'CS', 'N'),
       (321, 'MIT', 'history', 'N'),
       (321, 'MIT', 'psychology', 'N');
