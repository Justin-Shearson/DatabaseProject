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