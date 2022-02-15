import sqlite3
import json

from bottle import get, post, run, response, request

from contextlib import nullcontext
from distutils.log import debug
from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote
import random

db = sqlite3.connect("movies.sqlite")

def response(d):
    return json.dumps(d, indent=4) + "\n"

@get('/ping')
def ping():
    response.status = 200
    return "Pong\n"

@post('/reset')
def reset():
    c = db.cursor()
    c.execute("PRAGMA foreign_keys=OFF;")
    c.execute("DROP TABLE IF EXISTS Theaters;")
    c.execute("DROP TABLE IF EXISTS Screenings;")
    c.execute("DROP TABLE IF EXISTS Movies;")
    c.execute("DROP TABLE IF EXISTS Customers;")
    c.execute("DROP TABLE IF EXISTS Tickets;")
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
    c.execute("BEGIN TRANSACTION;")
    c.execute(
        """
        INSERT
        INTO    theaters(theater_name, capacity)
        VALUES  ('Kino',10),
                ('Regal', 16),
                ('Skandia, 100);
        """
    )
    c.execute("END TRANSACTION;")

    c.commit()
    response.status = 200
    return "tables reset\n"

# If given user name exists in db, does nothing and returns status code 400
# Otherwise adds user nad returns the string /users/<username> and status code 201
@post('/users')
def users():
    c = db.cursor()
    response.content_type = 'users/json'
    username = request.query.username
    customer_name = request.query.fullName
    password = request.query.pwd

    if not (username and customer_name and password):
        response.status = 400
        return response({"error": "Missing parameter"})

    query = """
        SELECT username, customer_name, password
        FROM   customers
        """,
    params = []
    if username:









@post('/movies')
def movies():
    c = db.cursor
    response.content_type = 'movies/json'
    imdbKey = request.query.imdbKey
    title = request.query.title
    year = request.query.year

    if not (imdbKey, title, year):
        response.status = 400
        return format({"error": "Missing parameter"})



run(host='localhost', port=7007, debug=True)
