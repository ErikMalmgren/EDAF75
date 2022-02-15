from contextlib import nullcontext
from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote

db = sqlite3.connect("movies.sqlite")

@get('/ping')
def ping():
    response.status = 200
    return "Pong\n"

@post('/reset')
def reset():
    c = db.cursor()
    c.execute("PRAGMA foreign_keys=OFF")
    c.execute("DROP TABLE IF EXITS theaters")
    c.execute("DROP TABLE IF EXITS screenings")
    c.execute("DROP TABLE IF EXITS movies")
    c.execute("DROP TABLE IF EXITS customers")
    c.execute("DROP TABLE IF EXITS tickets")
    c.execute("PRAGMA foreign_keys=ON")

    c.execute(
        """
        CREATE TABLE Movies (
        IMDB_key TEXT NOT NULL,
        title    TEXT NOT NULL,
        year    INT NOT NULL,
        runtime  INT NOT NULL,
        PRIMARY KEY (IMDB_key)
        );
        """
    )

    c.execute(
        """
        CREATE TABLE Customers (
        username        TEXT NOT NULL,
        customer_name   TEXT NOT NULL,
        password       TEXT NOT NULL,
        PRIMARY KEY (username)
        );
        """
    )

    c.execute(
        """
        CCREATE TABLE Screenings (
        theater_name TEXT NOT NULL,
        movie        TEXT NOT NULL,
        date         DATE NOT NULL,
        start_time   TIME NOT NULL,
        PRIMARY KEY (theater_name, movie, start_time, date),
        FOREIGN KEY (theater_name) REFERENCES Theaters(theater_name)
        );
        """
    )

    c.execute(
        """
        CREATE TABLE Theaters (
        theater_name        TEXT NOT NULL,
        capacity            INT NOT NULL,
        PRIMARY KEY (theater_name)
        );
        """
    )

    c.execute(
        """
        CREATE TABLE Tickets(
        ticketnumber   TEXT DEFAULT (lower(hex(randomblob(16)))),
        username       TEXT NOT NULL,
        date           DATE NOT NULL,
        time           TIME NOT NULL,
        movie          TEXT NOT NULL,
        theater_name   TEXT NOT NULL,
        PRIMARY KEY (ticketnumber),
        FOREIGN KEY (date, time, movie, theater_name)
        REFERENCES  Screenings(date, start_time, movie, theater_name)
        FOREIGN KEY (username)
        REFERENCES  Customers(username)
        );
        """
    )

    return "tables reset"




run(host='localhost', port=7007)
