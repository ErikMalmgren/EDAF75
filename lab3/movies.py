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
    c.execute("")

    return "tables reset"




run(host='localhost', port=7007)
