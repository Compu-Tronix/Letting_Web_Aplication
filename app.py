import mysql.connector
from flask import Flask, render_template, request, redirect, session
from tabulate import tabulate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'



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


'''

LISTS

'''
# registration list
reg_details = []

# user details list
user_details = []

# session identification list
session_identification = []


'''

FUNCTIONS

'''
# user authentication 
def user_authentication():
    username = request.form['username']
    password = request.form['password']
    user_details.append(username)
    user_details.append(password)
    print(username + password + 'appended to user_details')
    
    sql_login_statement = "select exists (select * from user where username=%s and password=%s);"
    cursor.execute(sql_login_statement, user_details)
    returned = cursor.fetchall()
    feedback = str(returned[0])
    result = int(feedback[1])
    
    if result == 1:
      set_session()
      user_details.clear()      
      print('user exists')
      return True

    elif result == 0:
      user_details.clear()
      print('user does not exist')
      return False
    
    else:
         print('user_authentication function error')

# set session
def set_session():
      sql_user_id_statement = "select id from user where username=%s and password=%s;"
      cursor.execute(sql_user_id_statement, user_details)
      returned = cursor.fetchall()
      feedback = str(returned[0])
      result = int(feedback[1])
      value = result
      session['id'] = value
      print('session has been initiated')
      return result

# session authentication
def session_authenticator():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + ' appended to session_identification list')

      sql_session_id_statement = "select exists (select id from user where id =%s);"
      cursor.execute(sql_session_id_statement, session_identification)
      returned = cursor.fetchall()
      feedback= str(returned[0])
      result= int(feedback[1])
      session_identification.clear()
      print('sql_session_id_statement returned: ' + str(result))

      if result == 1:
            return True
      
      elif result == 0 :
            return False
      
      else:
            print('session_authentication functon error')
      
        
'''

APPLICATION ROUTES

'''
# user login
@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        
        if user_authentication() == True:
             print('user logged on')
             return main()
        
        elif user_authentication() == False:
              print('user login failed')
              return logout()

        else:
              print('login function error')
              return main()


# user logout
@app.route('/logout/')
def logout():
      session.clear()
      return main()


# application start
@app.route('/', methods = ['POST','GET'])
def main():
      
      if session_authenticator() == True:
            logout = 'logout'
            dashboard = 'dashboard'
            return render_template ('index.html',logout=logout,dashboard=dashboard)
      
      elif session_authenticator() == False:
             login = 'login'
             dashboard = 'dashboard'
             return render_template ('index.html',login=login)
      
      else:
            print('failed to start app')
            return('an error occured')
             
    
if __name__ == '__main__':
    app.run (debug = False)