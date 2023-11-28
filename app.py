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

reg_details = []


@app.route('/', methods = ['POST','GET'])
def main():
    if request.method =='POST':
    
        username = request.form['username']
        surname = request.form['surname']
        cell_no = request.form['cell_no']
        email = request.form['email']
        password = request.form['password']

        def send_to_reg_details(reg_details):
            reg_details.append(username)
            reg_details.append(surname)
            reg_details.append(cell_no)
            reg_details.append(email)
            reg_details.append(password)
        send_to_reg_details(reg_details)
        print(reg_details)
        return'it worrks'
    
    else:
        print('error')
        return render_template ('index.html')


    




    
if __name__ == '__main__':
    app.run (debug = True)