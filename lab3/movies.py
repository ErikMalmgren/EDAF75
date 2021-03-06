from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote

db = sqlite3.connect("movies.sqlite")

def hash(password):
	import hashlib
	return hashlib.sha256(password.encode('utf-8')).hexdigest()


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
		imdb_key TEXT,
		title    TEXT,
		year     INT,
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
		username       TEXT,
		customer_name  TEXT,
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
		FOREIGN KEY  (imdb_key)     REFERENCES movies(imdb_key),
		FOREIGN KEY  (theater_name) REFERENCES Theaters(theater_name),
		PRIMARY KEY  (screening_id)
		);
		"""
	)

	c.execute(
		"""
		CREATE TABLE Tickets(
		ticketnumber   TEXT DEFAULT (lower(hex(randomblob(16)))),
		username       TEXT,
		screening_id,
		FOREIGN KEY (screening_id) REFERENCES screenings(screening_id)
		FOREIGN KEY (username)     REFERENCES customers(username),
		PRIMARY KEY (ticketnumber)
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
			[user['username'], user['fullName'], hash(user['pwd'])]
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

		screening_id, = c.fetchone()
		response.status = 201
		return f"/performances/{screening_id}"
	except sqlite3.IntegrityError:
		response.status = 400
		return "No such movie or theater"


@get('/performances')  # Now working as intended!
def get_performances():
	c = db.cursor()
	c.execute(
		"""
		WITH ticket_count(screening_id, ticketnumber) AS (
			SELECT   screening_id, count() AS ticketnumber
			FROM     tickets
			GROUP BY  screening_id
		) 
		SELECT   screenings.screening_id, date, start_time, title, year, theaters.theater_name, 
		theaters.capacity -  coalesce(ticketnumber, 0) AS number_ticket
		FROM     screenings
		JOIN     movies
		USING    (imdb_key)
		JOIN     theaters
		USING    (theater_name)
		LEFT OUTER JOIN ticket_count
		USING    (screening_id)
		"""
	)
	found = [{"performanceId": screening_id, "date": date, "startTime": start_time, "title": title, "year": year,
	          "theater": theater_name, "remainingSeats": number_ticket}
	         for screening_id, date, start_time, title, year, theater_name, number_ticket in c]
	response.status = 200
	return {"data": found}


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
	found = [{"imdbKey": imdb_key, "title": title, "year": production_year}
	         for imdb_key, title, production_year in c]
	response.status = 200
	return {"data": found}


@post('/tickets')
def purchase_tickets():
	ticket = request.json
	c = db.cursor()
	c.execute(
		"""
		SELECT    capacity - count(tickets.ticketnumber) AS remaining_seats
		FROM      screenings
		LEFT OUTER JOIN tickets ON tickets.screening_id = screenings.screening_id
		JOIN      theaters ON theaters.theater_name = screenings.theater_name
		WHERE     screenings.screening_id = ?
		""",
		[ticket["performanceId"]]
	)
	remaining_seats, = c.fetchone()
	if remaining_seats > 0:
		c.execute(
			"""
			SELECT    username
			FROM      customers
			WHERE     username = ? and password = ?
			""",
			[ticket["username"], hash(ticket["pwd"])]
		)
		user, = c.fetchone()
		if not user:
			response.status = 401
			return "Wrong user credentials"
		else:
			try:
				c.execute(
					"""
					INSERT INTO tickets (screening_id, username)
					VALUES      (?, ?)
					RETURNING   ticketnumber
					""",
					[ticket["performanceId"], ticket["username"]]
				)
				found, = c.fetchone()
				db.commit()
				response.status = 201
				return f"/tickets/{found}"
			except Exception as e:
				print(e)
				response.status = 400
				return "Error"
	else:
		response.status = 400
		return "No tickets left"


@get('/tickets')
def show_tickets():
	c = db.cursor()
	c.execute(
		"""
		SELECT    ticketnumber, screening_id, username
		FROM      tickets
		"""
	)
	found = [{"id": ticketnumber, "performanceId": screening_id, "username": username}
	         for ticketnumber, screening_id, username in c]
	response.status = 200
	return {"data": found}


@get('/users/<username>/tickets')
def get_user_tickets(username):
	c = db.cursor()
	c.execute(
		"""
		WITH ticket_count AS (
			SELECT  screenings.screening_id, count(tickets.ticketnumber) AS bought_tickets
			FROM    screenings
			LEFT OUTER JOIN  tickets ON tickets.screening_id = screenings.screening_id
			WHERE   username = ?
			GROUP BY  screenings.screening_id
		)
		SELECT    date, start_time, theaters.theater_name, title, year, bought_tickets
		FROM      screenings
		JOIN      movies ON screenings.imdb_key = movies.imdb_key
		JOIN      ticket_count ON screenings.screening_id  = ticket_count.screening_id
		JOIN      theaters ON theaters.theater_name = screenings.theater_name
		""",
		[username]
	)
	found = [{"date": date, "startTime": start_time, "theater": theater_name, "title": title, "year": year,
	          "nbrOfTickets": bought_tickets}
	         for date, start_time, theater_name, title, year, bought_tickets in c]
	response.status = 200
	return {"data": found}


run(host='localhost', port=7007, debug=True)
