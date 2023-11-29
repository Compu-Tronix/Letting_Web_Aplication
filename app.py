import mysql.connector
from flask import Flask, render_template, request, redirect
from tabulate import tabulate


app = Flask(__name__)


HOST = 'localhost'
DATABASE = 'letting_app'
USER = 'letting.app'
PASSWORD = 'letting@database'

db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
cursor = db_connection.cursor()
print(db_connection.get_server_info())

def ___repr__(self):
        
        return '<dashboard %r>' % self.id

def ___repr__(self):
        
        return '<login %r>' % self.id

def ___repr__(self):
        
        return '<logout %r>' % self.id



# registration list
reg_details = []

# user details list
user_details = []

# user authentication function
def user_authentication():
    sql_login_statement = "select exists (select * from user where username=%s and password=%s);"
    cursor.execute(sql_login_statement, user_details)
    result = cursor.fetchall()
    feedback= result[0]
    
    if str(feedback) == '(1,)':       
            print('user logged in')
            return True

    elif str(feedback) == '(0,)':
          print('user does not exist')
          return False


# user login
@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        def send_to_user_details(user_details):
            user_details.append(username)
            user_details.append(password)

        send_to_user_details(user_details)
        
        if user_authentication() == True:
             return main()
        
        elif user_authentication() == False:
              return logout()


# user logout
@app.route('/logout/')
def logout():
      user_details.clear()
      return main()


# application ignition
@app.route('/', methods = ['POST','GET'])
def main():
        if len(user_details) == 0:
             login = 'login'
             dashboard = 'dashboard'
             return render_template ('index.html',login=login)
        
        elif len(user_details) >= 1:
             logout = 'logout'
             dashboard = 'dashboard'
             return render_template ('index.html',logout=logout,dashboard=dashboard)
        
        else:
              print('failed')
              return('index.html')
             
    
if __name__ == '__main__':
    app.run (debug = True)