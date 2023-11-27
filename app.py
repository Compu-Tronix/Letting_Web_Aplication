import mysql.connector as mysql
from flask import Flask, render_template, request, redirect
from tabulate import tabulate

app = Flask(__name__)

HOST = 'localhost'
DATABASE = 'Letting_v-1.0.0'
USER = 'app1.0.0'
PASSWORD = ''

'''db_connection = mysql.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD)
print(db_connection.get_server_info())

cusor = db_connection.cursor()'''

@app.route('/')
def main():
    return render_template('guest/index.html')
    
if __name__ == '__main__':
    app.run (debug = True)