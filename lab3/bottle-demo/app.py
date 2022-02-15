from contextlib import nullcontext
from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote


db = sqlite3.connect("colleges.sqlite")


@get('/ping')
def ping():
    return {"200 OK" "\n" "Pong" "\n"}


@get('/reset')
def reset():
    return nullcontext

@get('/studentsSimple')
def get_students_simple():
    c = db.cursor()
    c.execute(
        """
        SELECT   s_id, s_name, gpa, size_hs
        FROM     students
        """
    )
    found = [{"id": s_id, "name": s_name, "gpa": gpa, "sizeHS": size_hs}
             for s_id, s_name, gpa, size_hs in c]
    response.status = 200
    return {"data": found}


@get('/students/<s_id>')
def get_student(s_id):
    c = db.cursor()
    c.execute(
        """
        SELECT   s_id, s_name, gpa, size_hs
        FROM     students
        WHERE    s_id = ?
        """,
        [s_id]
    )
    found = [{"id": s_id, "name": s_name, "gpa": gpa, "sizeHS": size_hs}
             for s_id, s_name, gpa, size_hs in c]
    response.status = 200
    return {"data": found}


@get('/students')
def get_students():
    query = """
        SELECT   s_id, s_name, gpa, size_hs
        FROM     students
        WHERE    1 = 1
        """
    params = []
    if request.query.name:
        query += " AND s_name = ?"
        params.append(unquote(request.query.name))
    if request.query.minGpa:
        query += " AND gpa >= ?"
        params.append(request.query.minGpa)
    c = db.cursor()
    c.execute(query, params)
    found = [{"id": s_id, "name": s_name, "gpa": gpa, "sizeHS": size_hs}
         for s_id, s_name, gpa, size_hs in c]
    response.status = 200
    return {"data": found}


@post('/students')
def post_student():
    student = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO       students(s_name, gpa, size_hs)
        VALUES     (?, ?, ?)
        RETURNING  s_id
        """,
        [student['name'], student['gpa'], student['sizeHS']]
    )
    found = c.fetchone()
    if not found:
        response.status = 400
        return "Illegal..."
    else:
        response.status = 201
        s_id, = found
        return f"http://localhost:3000/{s_id}"


@get('/students/<s_id>/applications')
def get_students(s_id):
    c = db.cursor()
    c.execute(
        """
        SELECT  s_id, c_name, major, decision
        FROM    applications
        JOIN    students
        USING   (s_id)
        WHERE   s_id = ?
        """,
        [s_id]
    )
    found = [{"id": s_id, "college": c_name, "major": major, "decision": decision} 
             for s_id, c_name, major, decision in c]
    response.status = 200
    return {"data": found}


run(host='localhost', port=7007)
