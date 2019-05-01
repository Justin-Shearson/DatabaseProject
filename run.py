import configparser
from flask import Flask, render_template, request, url_for, redirect, request
import mysql.connector
import time
import datetime
import json

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
			return redirect(url_for('events',user=username))
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
@app.route("/addevent/<username>", methods=['GET', 'POST'])
def addevent(username):
	if userIsOrganizer(username):
		if request.method == 'POST':
			event_name = str(request.form['name'])
			organization = str(request.form['organization'])
			caterer = str(request.form['caterer'])
			date = str(request.form['date'])
			price = int(request.form['price'])
			location = str(request.form['location'])
			database = mysql.connector.connect(**config['mysql.connector'])
			sqldict = generateInsertQuery(event_name,date,organization,caterer,price,location)
			cursor = database.cursor()
			print(sqldict["event_insert"])
			print(sqldict["lead_insert"])
			print(sqldict["catered_insert"])
			cursor.execute(sqldict["event_insert"])
			cursor.execute(sqldict["lead_insert"])
			cursor.execute(sqldict["catered_insert"])
			database.commit()			
			cursor.close()
			database.close()
		return render_template('add.html')
	return "Illegal Access"

def generateInsertQuery(event_name,date, organization, caterer, price, location):
	event_insert =  "INSERT INTO Events SET name = '" + event_name + "', dates ='" + date + "', price =CAST('" + str(price) + "' as DECIMAL), location_id = ( Select l.id from Locations l where l.name = '" + location + "');"
	lead_insert = "INSERT INTO lead_by (event_id, organization_id) SELECT e.id, o.id from Organizations o, Events e where e.name = '"+ event_name +"' AND o.name = '" + organization + "';"
	catered_insert = "INSERT INTO catered_by (event_id, caterer_id) select e.id, c.id from Caterers c, Events e where e.name = '" +event_name + "' AND c.name = '" + caterer + "';"
	returndict = {
		'event_insert' : event_insert,
		'lead_insert' : lead_insert,
		'catered_insert' : catered_insert
	}
	return returndict

@app.route("/deleteevent/<username>/", methods=['GET','POST'])
def deleteevent(username):
	if userIsOrganizer(username):
		if request.method == 'POST':
			event_id = str(request.form['event_id'])
			sqldict = generatedeletequery(event_id)
			database = mysql.connector.connect(**config['mysql.connector'])
			cursor = database.cursor()
			print(sqldict["event_delete"])
			print(sqldict["catered_by_delete"])
			print(sqldict["lead_by_delete"])
			cursor.execute(sqldict["catered_by_delete"])
			cursor.execute(sqldict["lead_by_delete"])
			cursor.execute(sqldict["event_delete"])
			database.commit()	
			cursor.close()
			database.close()
		sql = """SELECT e.id, e.name, e.dates, l2.name, c2.name,o.name,e.price from Events e 
		JOIN catered_by c on e.id = c.event_id and e.dates > now()
		JOIN lead_by l on e.id = l.event_id 
		JOIN Organizations o on o.id = l.organization_id
		JOIN Users u on u.name = '""" + username + """'
		JOIN member_of m on m.user_id = u.id and o.id = m.organization_id
		JOIN Locations l2 on l2.id= e.location_id 
		JOIN Caterers c2 on c2.id = c.caterer_id;"""
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()
		print(sql)
		cursor.execute(sql)
		returnlist = cursor.fetchall()
		return render_template('delete.html', results = returnlist)
	return "Illegal Access"

@app.route("/updateevent/<username>/" , methods=['GET','POST'])
def updateevent(username):
	if userIsOrganizer(username):
		if request.method == 'POST':
			event_id = str(request.form['event_id'])
			caterer = str(request.form['caterer'])
			date = str(request.form['date'])
			price = int(request.form['price'])
			location = str(request.form['location'])
			sqldict= generateupdatequery(event_id,caterer,date,price,location)
			database = mysql.connector.connect(**config['mysql.connector'])
			cursor = database.cursor()
			print(sqldict["event_update"])
			print(sqldict["catered_by_delete"])
			print(sqldict["catered_insert"])
			cursor.execute(sqldict["catered_by_delete"])
			cursor.execute(sqldict["catered_insert"])
			cursor.execute(sqldict["event_update"])
			database.commit()	
			cursor.close()
			database.close()
		sql = """SELECT e.id, e.name, e.dates, l2.name, c2.name,o.name,e.price from Events e 
		JOIN catered_by c on e.id = c.event_id and e.dates > now()
		JOIN lead_by l on e.id = l.event_id 
		JOIN Organizations o on o.id = l.organization_id
		JOIN Users u on u.name = '""" + username + """'
		JOIN member_of m on m.user_id = u.id and o.id = m.organization_id
		JOIN Locations l2 on l2.id= e.location_id 
		JOIN Caterers c2 on c2.id = c.caterer_id;"""
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()
		print(sql)
		cursor.execute(sql)
		returnlist = cursor.fetchall()
		return render_template('update.html', results = returnlist)
	return "Illegal Access"

def generateupdatequery(event_id, caterer, date, price, location):
	event_update = "UPDATE Events SET dates = '" + date + "', price =CAST('" + str(price) + "' as DECIMAL), location_id = (select l.id from Locations l where l.name = '" + location + "') WHERE Events.id = CAST('" + str(event_id) + "' as UNSIGNED);"
	catered_by_delete = "Delete from catered_by where catered_by.event_id = CAST('" + str(event_id) + "' as UNSIGNED)"
	catered_insert = "INSERT INTO catered_by (event_id, caterer_id) SELECT CAST('" + str(event_id) + "' as UNSIGNED), c.id from Caterers c WHERE c.name = '" + caterer + "';"
	returndict = {
		"event_update" : event_update,
		"catered_by_delete" : catered_by_delete,
		"catered_insert" : catered_insert
	}
	return returndict

def generatedeletequery(event_id):
	event_delete = "Delete from Events where Events.id = CAST('" + str(event_id) + "' as UNSIGNED)" 
	catered_by_delete = "Delete from catered_by where catered_by.event_id = CAST('" + str(event_id) + "' as UNSIGNED)"
	lead_by_delete = "Delete from lead_by where lead_by.event_id = CAST('" + str(event_id) + "' as UNSIGNED)"
	returndict = {
		"event_delete" : event_delete,
		"catered_by_delete" : catered_by_delete,
		"lead_by_delete" : lead_by_delete
	}
	return returndict

@app.route("/allevents", methods=['GET','POST'])
def allevents():
	if request.method == 'GET':
		sql = "SELECT e.name, e.dates, l2.name, c2.name,o.name,e.price from Events e JOIN catered_by c on e.id = c.event_id and e.dates > now() JOIN lead_by l on e.id = l.event_id JOIN Locations l2 on l2.id= e.location_id JOIN Caterers c2 on c2.id = c.caterer_id JOIN Organizations o on o.id = l.organization_id;"
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()
		cursor.execute(sql)
		returnlist = cursor.fetchall()

		return render_template('allevents.html', results = returnlist)
	return "You died"


@app.route("/freeevents", methods=['GET','POST'])
def freeevents():
	if request.method == 'GET':
		sql = "SELECT e.name, e.dates, l2.name, c2.name,o.name from Events e JOIN catered_by c on e.id = c.event_id and e.dates > now() and e.price = 0 JOIN lead_by l on e.id = l.event_id JOIN Locations l2 on l2.id= e.location_id JOIN Caterers c2 on c2.id = c.caterer_id JOIN Organizations o on o.id = l.organization_id;"
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()
		cursor.execute(sql)
		returnlist = cursor.fetchall()

		return render_template('free.html', results = returnlist)
	return "You died"

@app.route("/updateuser/<username>/", methods=['GET','POST'])
def updateuser(username):
	if request.method =='POST':
		username = str(request.form[''])
		password = str(request.form['password'])
		print(password)
		location = str(request.form['location'])
		print(location)
		caterer = str(request.form['caterer'])
		user_query = generateupdateuserquery(username, password, location)
		database = mysql.connector.connect(**config['mysql.connector'])
		cursor = database.cursor()
		if user_query is not None:
			cursor.execute(user_query)
		if caterer is not None:
			caterer_query = "INSERT INTO prefers(user_id, caterer_id) SELECT u.id , c.id from User u join Caterers c on u.name = '"+username+"' and c.name = '" + caterer + "';"
			cursor.execute(caterer_query)
		database.commit()	
		cursor.close()
		database.close()
	return render_template('account.html')

def generateupdateuserquery(username,password,location):
	update_user = "UPDATE Users SET "
	if location is None and password is None:
		return None
	if location is not None:
		update_user = update_user + "Users.location_id = (Select l.id from Locations l where l.name = '" + location + "'),"
	if password is not None:
		update_user = update_user + "User.password = '" + password + "'"
	else:
		update_user = update_user[:-1]
	update_user = update_user + "WHERE Users.name = '" + username +"';"
	return update_user

def convertdatetime(date):
    return datetime.datetime.strptime (date, '%m/%d/%Y').strftime ('%Y-%m-%d')


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

def userIsOrganizer(username):
	sql = "SELECT name FROM Users WHERE Users.name = \'{}\' and Users.is_organizer = 1".format(username)
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	user = cursor.fetchone()
	cursor.close()
	database.close()
	return user is not None



#Currently used to route to the second page of the website
@app.route('/events/<user>')
def events(user):
	sql = "Select count(e.id) from Events e where e.dates > now() and e.price = 0"
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.cursor()
	cursor.execute(sql)
	count = cursor.fetchone()
	truecount = count[0]
	print(count)
	return render_template('events.html',user = user, count = truecount)

#Run the server
if __name__ == '__main__':
	app.run(**config['app'])
