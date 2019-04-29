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
	curosr = database.cursor()
	cursor.execute(sql)
	database.commit()
	cursor.close()
	db.close()

#Executes a login check to make sure that the username does not already exist
@app.route("/execlogin", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = str(request.form['username'])
		password = str(request.form['password'])
		database = mysql.connector.connect(**config['mysql.connector'])
		curosr = database.cursor()
		cursor.execute("SELECT name FROM Users u WHERE u.name = %s and u.password = %s", (username, password))
		user = cursor.fetchone()
		cursor.close()
		database.close()
		if len(user) is 1:
			return redirect(url_for('index'))
		else:
			return "Username or password is incorrect!"
	return render_template('loginpage.html')

#Routes to the page to check if the input username is already in use
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = str(request.form['username'])
		password = str(request.form['password'])
		organizer = str(request.form['organizer'])
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.curosr()
		cursor.execute("SELECT name FROM Users u WHERE u.name = %s and u.password = %s", (username, password, organizer))
		user = cursor.fetchall()

		#If the user already exists
		if len(user) != 0:
			cursor.close()
			database.close()
			return "That username already exists"
		else:
			execsignup(username, password, organizer)
			user = cursor.fetchone()
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
	cursor = database.curosr()
	cursor.execute("SELECT")

#Used to render the webpage for the main website
@app.route('/')
def index():
	return render_template('index.html')

def execsignup(username, password, IsOrganizer):
	sql = "INSERT INTO Users(name, password, IsOrganizer) VALUES({},{},{})".format(username,password,IsOrganizer)
	database = mysql.connector.connect(**config['mysql.connector'])
	curosr = database.cursor()
	cursor.execute(sql)
	cursor.commit()
	cursor.close()
	database.close()


#Currently used to route to the second page of the website
@app.route('/events')
def events():
	return render_template('events.html')

#Currently used to route to the login page of the website
@app.route('/login', methods = ['GET', 'POST'])
def loginpage():
	if request.method == "POST":
		contents = request.form
		username = contents['uname']
		password = contents['psw']
	return render_template('login.html')

#Run the server
if __name__ == '__main__':
	app.run(**config['app'])