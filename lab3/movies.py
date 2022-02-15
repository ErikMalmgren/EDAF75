from contextlib import nullcontext
from distutils.log import debug
from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote
import random

db = sqlite3.connect("movies.sqlite")

@get('/ping')
def ping():
    response.status = 200
    return "Pong\n"

@post('/reset')
def reset():
    c = db.cursor()
    c.execute("PRAGMA foreign_keys=OFF;")
    c.execute("DROP TABLE IF EXITS Theaters;")
    c.execute("DROP TABLE IF EXITS Screenings;")
    c.execute("DROP TABLE IF EXITS Movies;")
    c.execute("DROP TABLE IF EXITS Customers;")
    c.execute("DROP TABLE IF EXITS Tickets;")
    c.execute("PRAGMA foreign_keys=ON;")

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
        CREATE TABLE Screenings (
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

@post('/users')
def users():
    c = db.cursor()
    c.execute(
        """
        
        
        """
    )



run(host='localhost', port=7007, debug=True)
