PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS Tickets;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Screenings;
DROP TABLE IF EXISTS Theaters;

PRAGMA foreign_keys=ON;

CREATE TABLE Movies (
    IMDB_key TEXT NOT NULL,
    title    TEXT NOT NULL,
    year    INT NOT NULL,
    runtime  INT NOT NULL,

    PRIMARY KEY (IMDB_key)
);

CREATE TABLE Customers (
    username        TEXT NOT NULL,
    customer_name   TEXT NOT NULL,
    password       TEXT NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE Theaters (
    theater_name        TEXT NOT NULL,
    capacity            INT NOT NULL,
    PRIMARY KEY (theater_name)
);


CREATE TABLE Screenings (
    theater_name TEXT NOT NULL,
    movie        TEXT NOT NULL,
    date         DATE NOT NULL,
    start_time   TIME NOT NULL,
    PRIMARY KEY (theater_name, movie, start_time, date),
    FOREIGN KEY (theater_name) REFERENCES Theaters(theater_name)
  --FOREIGN KEY (movie) REFERENCES Movies(title)
);


CREATE TABLE Tickets(
    ticketnumber   TEXT DEFAULT (lower(hex(randomblob(16)))),
    username       TEXT NOT NULL,
    date           DATE NOT NULL,
    time           TIME NOT NULL,
    movie          TEXT NOT NULL,
    theater_name   TEXT NOT NULL,
    PRIMARY KEY (ticketnumber),
    FOREIGN KEY (username, date, time, movie, theater_name)
    REFERENCES  Screenings(username, date, start_time, movie, theater_name)
    FOREIGN KEY (username)
    REFERENCES  Customers(username)
);

BEGIN TRANSACTION;

INSERT
INTO    Theaters (theater_name, capacity)
VALUES  ('Spegeln', 137),
        ('Filmstaden', 156),
        ('Kårhuset', 1337),
        ('E Huset', 420);

INSERT
INTO    Movies (IMDB_key, title, year, runtime)
VALUES  ('tt1636826', 'Project X', 2012, 88),
        ('tt0126029', 'Shrek', 2001, 90),
        ('tt7286456', 'Joker', 2019, 122),
        ('tt0462538', 'The Simpsons', 2007, 87);

INSERT
INTO    Screenings(theater_name, movie, date, start_time)
VALUES  ('Spegeln', 'Project X', '2022-02-09', '13:37:42'),
        ('Spegeln', 'Project X', '2022-02-09', '23:12:10'),
        ('Filmstaden', 'Project X', '2022-02-09', '13:37:42'),
        ('Kårhuset', 'Joker', '2022-02-14', '09:09:09'),
        ('E Huset', 'Shrek', '2022-04-20', '06:09:42');

INSERT
INTO    Customers (username, customer_name, password)
VALUES  ('Slayerking1337', 'Adam Bertilsson', 'kaffe123'),
        ('pogman', 'Isak Määttä', 'password'),
        ('JennyDover', 'Erik Malmgren', '123456'),
        ('tjoggepamp', 'Bdam Aertilsson', 'hej');

END TRANSACTION;
