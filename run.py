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

@app.route("/execlogin", methods=['GET', 'POST'])
def login():
	username = str(request.form['username'])
	password = str(request.form['password'])
	database = mysql.connector.connect(**config['mysql.connector'])
	curosr = database.cursor()
	cursor.execute("SELECT name FROM Users u WHERE u.name = %s and u.password = %s", (username, password))
	user = cursor.fetchone()
	cursor.close()
	database.close()
	if len(user) is 1:
		return redirect(url_for('index'),)
	else:
		return "Username or password is incorrect!"

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	username = str(request.form['username'])
	password = str(request.form['password'])
	organizer = str(request.form['organizer'])
	database = mysql.connector.connect(**config['mysql.connector'])
	cursor = database.curosr()
	cursor.execute("SELECT name FROM Users u WHERE u.name = %s and u.password = %s", (username, password))
	user = cursor.fetchall()

	if len(user) != 0:
		cursor.close()
		database.close()
		return "That username already exists"
	else:
		cursor.execute("INSERT INTO Users(name, password, IsOrganizer) VALUES(%s, %s, %s)", (username, password, organizer))
		cursor.execute("SELECT name FROM Users u WHERE u.name = %s and u.password = %s", (username, password))
		user = cursor.fetchone()
		cursor.close()
		database.close()
		return redirect(url_for('index'))

def index():
	return render_template('index.html')

@app.route('/')
def template_response():
	return render_template('index.html')

# @app.route('/', methods=['GET', 'POST'])
# def index():
# 	return render_template('index.html')

@app.route('/secondpage')
def secondpage():
	return render_template('secondpage.html')

if __name__ == '__main__':
	app.run(**config['app'])