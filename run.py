import configparser
from flask import Flask, render_template, request, url_for, redirect, request
import mysql.connector
import time
import datetime

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
			return redirect(url_for('events'))
	return render_template('login.html')

#Routes to the page to check if the input username is already in use
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		username = str(request.form['username'])
		password = str(request.form['password'])
		organization = int(request.form['organization'])
		IsOrganizer = 0
		if organization is not 0:
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
			sql = "INSERT INTO Users(name, password, is_organizer) VALUES(\'{}\',\'{}\',{})".format(username,password,IsOrganizer)
			cursor.execute(sql)
			database.commit()
			if IsOrganizer is 1:
				cursor.execute("SELECT id FROM Users WHERE Users.name =\'{}\'".format(username))
				user = cursor.fetchone()
				userid = user[0]
				assignorganizer(userid, organization)

			cursor.close()
			database.close()
			return redirect(url_for('login'))
	return render_template('signup.html')

#Routes to the addevent page to add an event to the website
@app.route("/addevent", methods=['GET', 'POST'])
def addevent(username, organization):
	if userIsOrganizer(username)
		if request.method == 'POST':
			event_name = str(request.form['name'])
			organization = str(request.form['organization'])
			caterer = str(request.form['caterer'])
			date = str(request.form['date'])
			price = int(request.form['price'])
			location = str(request.form['location'])
			database = mysql.connector.connect(**config['mysql.connector'])
			sql = generateInsertQuery(event_name,date,organization,caterer,price,location)
			cursor = database.cursor(sql)
			cursor.execute()
			cursor.close()
			database.close()
		return render_template('addevents.html')
	return "Illegal Access"

def convertdatetime(date):
    return datetime.datetime.strptime (date, '%m/%d/%Y').strftime ('%Y-%m-%d')

def generateInsertQuery(event_name,date, organization, caterer, price, location):
	return "INSERT INTO Events SET name = '" + event_name + "', dates ='" + convertdatetime(date) +
	"', location_id = ( Select l.id from Locations l where l.id = '" + location + "');" +
	"INSERT INTO lead_by (event_id, organization_id) SELECT e.id, o.id from Organizations o, Events e where e.name = '"+
	event_name +"' AND o.name = '" + organization + "';"+
	"INSERT INTO catered_by (event_id, caterer_id) select e.id, c.id from Cateres c, Events e where e.name = '" +
	event_name + "' AND c.name = '" + caterer + "';"
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

def userIsOrganizer(username)
	sql = "SELECT name FROM Users WHERE Users.name = \'{}\' and Users.is_organizer = 1".format(username)
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	user = cursor.fetchone()
	cursor.close()
	database.close()
	return user is not None



#Currently used to route to the second page of the website
@app.route('/events')
def events():
	return render_template('events.html')

#Run the server
if __name__ == '__main__':
	app.run(**config['app'])