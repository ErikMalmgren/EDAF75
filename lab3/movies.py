from contextlib import nullcontext
from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote

db = sqlite3.connect("movies.sqlite")

@get('/ping')
def ping():
    return {"200 OK" "\n" "Pong" "\n"}
    
run(host='localhost', port=7007)
