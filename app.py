import mysql.connector
from flask import Flask, render_template, request, redirect
from tabulate import tabulate

app = Flask(__name__)

HOST = 'localhost'
DATABASE = 'letting_app'
USER = 'letting.app'
PASSWORD = 'letting@database'

db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
print(db_connection.get_server_info())

cusor = db_connection.cursor()

@app.route('/')
def main():
    return render_template('guest/index.html')
    
if __name__ == '__main__':
    app.run (debug = True)