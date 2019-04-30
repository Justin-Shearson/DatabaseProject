import configparser
from flask import Flask, render_template, request, url_for, redirect, request
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

def query(sql):
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	cursor.close()
	database.close()
	return result

def execute(sql):
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	database.commit()
	cursor.close()
	db.close()

#Executes a login check to make sure that the username does not already exist
@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = str(request.form['username'])
		password = str(request.form['password'])
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()
		cursor.execute("SELECT name FROM Users u WHERE u.name = %s and u.password = %s", (username, password))
		user = cursor.fetchone()
		cursor.close()
		database.close()
		if user is None:
			return "Username or password is incorrect!"
		else:
			return redirect(url_for('index'))
	return render_template('login.html')

#Routes to the page to check if the input username is already in use
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = str(request.form['username'])
		password = str(request.form['password'])
		organization = str(request.form['organization'])
		IsOrganizer = 0
		if organization != 0:
			IsOrganizer = 1
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()		
		cursor.execute("SELECT name FROM Users WHERE Users.name = \'{}\'".format(username))
		user = cursor.fetchone()

		#If the user already exists
		if user is not None:
			cursor.close()
			database.close()
			return redirect(url_for('signup'))

		else:
			# execsignup(username, password, IsOrganizer, cursor)
			sql = "INSERT INTO Users(name, password, IsOrganizer) VALUES(\'{}\',\'{}\',{})".format(username,password,IsOrganizer)
			cursor.execute(sql)
			database.commit()
			if IsOrganizer == 1:
				cursor.execute("SELECT Id FROM Users WHERE Users.name =\'{}\'".format(username))
				user = cursor.fetchone()
				userid = user[0]
				assignorganizer(userid, organization)

			cursor.close()
			database.close()
			return redirect(url_for('index'))
	return render_template('signup.html')

#Routes to the addevent page to add an event to the website
@app.route("/addevent", methods=['GET', 'POST'])
def addevent():
	username = str(request.form['username'])
	organizer = str(request.form['organizer'])
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute("SELECT")
	return render_template('addevent.html')

#Used to render the webpage for the main website
@app.route('/')
def index():
	return render_template('index.html')

#Helper function for the signup page. Executed when the user attempts to sign into the database
def execsignup(username, password, IsOrganizer, cursor):
	sql = "INSERT INTO Users(name, password, IsOrganizer) VALUES(\'{}\',\'{}\',{})".format(username,password,IsOrganizer)
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	cursor.close()
	database.close()

def assignorganizer(userid, organization):
	sql = "INSERT INTO member_of VALUES({},{})".format(userid,organization)
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	database.commit()
	cursor.close()
	database.close()

#Currently used to route to the second page of the website
@app.route('/events')
def events():
	return render_template('events.html')

#Run the server
if __name__ == '__main__':
	app.run(**config['app'])