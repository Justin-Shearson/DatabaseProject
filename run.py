import configparser
from flask import Flask, render_template, request
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

def query(sql):


if __name__ == '__main__';
	app.run(**config['app'])