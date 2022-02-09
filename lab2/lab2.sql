PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS Tickets;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Screenings;
DROP TABLE IF EXISTS Theaters;

PRAGMA foreign_keys=ON;


CREATE TABLE Theaters (
    theater_name        TEXT NOT NULL,
    capacity            INT NOT NULL,
    PRIMARY KEY (theater_name, capacity)
);


CREATE TABLE Screenings (
    theater_name TEXT NOT NULL,
    movie        TEXT NOT NULL,
    date_        DATE NOT NULL,
    start_time   TIME NOT NULL;
    PRIMARY KEY (theater_name, movie, start_time),
    FOREIGN KEY (theater_name) REFERENCES Theaters(theatrer_name),
    FOREIGN KEY (movie) REFERENCES Movies (title)
);


CREATE TABLE Movies (
    IMDB_key TEXT NOT NULL,
    title    TEXT NOT NULL,
    year_     INT NOT NULL,
    runtime  INT NOT NULL,

    PRIMARY KEY (IMDB_key)
);


CREATE TABLE Customers (
    username        TEXT NOT NULL,
    customer_name   TEXT NOT NULL,
    password_       TEXT NOT NULL,
    PRIMARY KEY (username)
);


CREATE TABLE Tickets(
    ticketnumber   TEXT DEFAULT (lower(hex(randomblob(16)))),
    username       TEXT NOT NULL,
    date_           DATE NOT NULL,
    time_           TIME NOT NULL,
    movie          TEXT NOT NULL,
    PRIMARY KEY (ticketnumber),
    FOREIGN KEY (username) REFERENCES Customers(username),
    FOREIGN KEY (date_) REFERENCES Screenings(date_),
    FOREIGN KEY (time_) REFERENCES Screenings(time_),
    FOREIGN KEY (movie) REFERENCES Movies(title)
);


INSERT
INTO    Theaters (theater_name, capacity)
VALUE   ('Spegeln', 137),
        ('Filmstaden', 156),
        ('Kårhuset', 1337),
        ('E Huset', 420);

INSERT 
INTO    Movies (IMDB_key, title, year, runtime)
VALUE   ('tt1636826', 'Project X', 2012, 88),
        ('tt0126029', 'Shrek', 2001, 90),
        ('tt7286456', 'Joker', 2019, 122),
        ('tt0462538', 'The Simpsons', 2007, 87);

INSERT
INTO    Screenings(theater_name, movie, date, time)
VALUE   ('Spegeln', 'Project X', '2022-02-09', '13:37:42'),
        ('Spegeln', 'Project X', '2022-02-09', '23:12:10'),
        ('Filmstaden', 'Project X', '2022-02-09', '13:37:42'),
        ('Kårhuset', 'Joker', '2022-02-14', '09:09:09'),
        ('E Huset', 'Shrek', '2022-04-20', '06:09:42');

INSERT 
INTO    Customers (username, customer_name, password)
VALUE   ('Slayerking1337', 'Adam Bertilsson', 'kaffe123'),
        ('pogman', 'Isak Määttä', 'password'),
        ('JennyDover', 'Erik Malmgren', '123456'),
        ('tjoggepamp', 'Bdam Aertilsson', 'hej');

