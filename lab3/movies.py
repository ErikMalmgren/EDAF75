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
        imdb_key     TEXT,
        date         DATE,
        start_time   TIME,
        screening_id TEXT DEFAULT  (lower(hex(randomblob(16)))),
        PRIMARY KEY  (screening_id),
        FOREIGN KEY  (theater_name) REFERENCES Theaters(theater_name)
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
                ('Skandia', 100);
        """
    )
    c.execute("END TRANSACTION;")

    db.commit()
    response.status = 200
    return "tables reset\n"

# If given username exists in db, does nothing and returns status code 400
# Otherwise adds user nad returns the string /users/<username> and status code 201
@post('/users')
def post_users():
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
def post_movie():
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
def post_performances():
    performance = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO   screenings(theater_name, imdb_key, date, start_time)
            VALUES (?, ?, ?, ?)
            """,
            [performance['theater'], performance['imdbKey'], performance['date'], performance['time']]
        )
        db.commit()

        c.execute(
            """
            SELECT screening_id
            FROM   screenings
            WHERE  rowid = last_insert_rowid()
            """
        )

        screening_id = c.fetchone()

        response.status = 201
        return f"/performances/{screening_id}"
    except sqlite3.IntegrityError:
        response.status = 400
        return "No such movie or theater"

@get('/performances')
def get_performances():
    c = db.cursor()
    query = """
            SELECT   screening_id, date, start_time, imdb_key, year, theater_name, capacity
            FROM     screenings
            JOIN     theaters
            USING    (theater_name)
            JOIN     movies
            USING    (imdb_key)
            WHERE    1 = 1
            """
    c.execute(query)
    performances = c.fetchall()
    print(performances)
    return {"data:" : performances}






@get('/movies')
def get_movies():
    c = db.cursor()
    query = """
            SELECT   imdb_key, title, year
            FROM     movies
            WHERE    1 = 1
            """
    params = []
    if request.query.title:
        query += " AND title = ?"
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND year >= ?"
        params.append(request.query.year)
    c.execute(query, params)
    found = [{"imdbKey": imdb_key, "title": title, "year": year}
             for imdb_key, title, year in c]
    print(found)
    response.status = 200
    return {"data": found}

@get('/movies/<imdb_key>')
def get_movie_imdbKey(imdb_key):
    c = db.cursor()
    c.execute(
          """
          SELECT  imdb_key, title, year
          FROM    movies
          WHERE   imdb_key = ?
          """,
          [imdb_key]
      )
    found = [{"imdbKey":imdb_key,"title": title, "year":production_year}
            for imdb_key, title, production_year in c]
    response.status = 200
    return {"data": found}





run(host='localhost', port=7007, debug=True)
