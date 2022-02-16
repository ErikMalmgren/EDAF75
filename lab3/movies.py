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
        IMDB_key TEXT NOT NULL,
        title    TEXT NOT NULL,
        year    INT NOT NULL,
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
        screening_id TEXT DEFAULT  (lower(hex(randomblob(16))))
        PRIMARY KEY  (screening_id),
        FOREIGN KEY  (theater_name) REFERENCES Theaters(theater_name)
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

# If given username exists in db, does nothing and returns status code 400
# Otherwise adds user nad returns the string /users/<username> and status code 201
@post('/users')
def users():
    c = db.cursor()
    user = request.json
    username = user['username']
    full_name = user['fullName']
    pwd = user['pwd'] # Behöver hashas

    if not (username and full_name and pwd):
        response.status = 400
        return response({"error": "Missing parameter"})

    try:
        c.execute(
            """
            INSERT
            INTO    customers(username, customer_name, password)
            VALUES  (?, ?, ?)
            """,
            [user['username'], user['customer_name'], user['password']]
                )
        db.commit()
        response.status = 201
        return f"/users{user['username']}"

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
            INTO   screenings(theater_name, movie, date, time)
            VALUES (?, ?, ?, ?)
            """,
            [performance['theater'], performance['imdbKey'], performance['date'], performance['time']]
        )
        db.commit()
        response.status = 201
        return f"/performances/"



run(host='localhost', port=7007, debug=True)
