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
    return "pong\n"

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

    # Apparently c.execute("DELETE FROM *table*") works
    c.execute(
        """
        CREATE TABLE Movies (
        IMDB_key TEXT,
        title    TEXT,
        year    INT,
        runtime  INT,
        PRIMARY KEY (IMDB_key)
        );
        """
    )
    # För att undvika dubletter kan man använda UNIQUE() i sitt query (Vet inte om Isak har tänkt på detta)
    # https://stackoverflow.com/questions/29312882/sqlite-preventing-duplicate-rows
    c.execute(
        """
        CREATE TABLE Customers (
        username        TEXT,
        customer_name   TEXT,
        password       TEXT,
        PRIMARY KEY (username)
        );
        """
    )

    c.execute(
        """
        CREATE TABLE Theaters (
        theater_name        TEXT,
        capacity            INT,
        PRIMARY KEY (theater_name)
        );
        """
    )

    c.execute(
        """
        CREATE TABLE Screenings (
        theater_name TEXT,
        movie        TEXT,
        date         DATE,
        start_time   TIME,
        screening_id TEXT DEFAULT  (lower(hex(randomblob(16)))),
        PRIMARY KEY  (screening_id),
        FOREIGN KEY  (theater_name) REFERENCES Theaters(theater_name),
        FOREIGN KEY  (movie) REFERENCES movies(title)
        );
        """
    )

    

    c.execute(
        """
        CREATE TABLE Tickets(
        ticketnumber   TEXT DEFAULT (lower(hex(randomblob(16)))),
        username       TEXT,
        date           DATE,
        time           TIME,
        movie          TEXT,
        theater_name   TEXT,
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

# If given username exists in db, does nothing and returns status code 400
# Otherwise adds user nad returns the string /users/<username> and status code 201
@post('/users')
def users():
    c = db.cursor()
    user = request.json

    try:
        c.execute(
            """
            INSERT
            INTO    customers(username, customer_name, password)
            VALUES  (?, ?, ?)
            """,
            [user['username'], user['fullName'], user['pwd']]
                )
        db.commit()
        response.status = 201
        return f"/users/{user['username']}"

    except sqlite3.IntegrityError:
        response.status = 400
        return ""



# Kanske att vi måste plocka bort runtime, det är inte med i exemplet på JSON objekt
@post('/movies')
def movie():
    movie = request.json 
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO movies(imdb_key, title, year)
            VALUES (?, ?, ?)
            """,
            [movie['imdbKey'], movie['title'], movie['year']] 
                )
        db.commit()
        response.status = 201
        return f"/movies/{movie['imdbKey']}"
        
    except sqlite3.IntegrityError:
        response.status = 400
        return ""


@post('/performances')
def performances():
    performance = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO   screenings(theater_name, movie, date, start_time)
            VALUES (?, ?, ?, ?)
            """,
            [performance['theater'], performance['imdbKey'], performance['date'], performance['time']]
        )
        response.status = 201
        return f"/performances/whack"
    except sqlite3.IntegrityError:
        response.status = 400
        return "No such movie or theater"



run(host='localhost', port=7007, debug=True)
