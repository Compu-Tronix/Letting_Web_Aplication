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

# clean data
def clean_data(value):
      x = value
      del_suffix = x[:-3]
      del_prefix = del_suffix[:0] + del_suffix[2:]
      cleaned_data = del_prefix
      return cleaned_data

# username
def get_username():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_get_username = "select username from user where id =%s;"
      cursor.execute(sql_get_username, session_identification)
      returned = cursor.fetchall()
      session_identification.clear()
      user_name = str(returned[0])
      print(clean_data(user_name))
     
      return  clean_data(user_name)

# surname
def get_surname():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_get_surname = "select surname from user where id =%s;"
      cursor.execute(sql_get_surname, session_identification)
      returned = cursor.fetchall()
      session_identification.clear()
      surname = str(returned[0])
      print(clean_data(surname))
      
      return clean_data(surname)

# id_number
def get_id_number():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_get_id_number = "select id_no from user where id =%s;"
      cursor.execute(sql_get_id_number, session_identification)
      returned = cursor.fetchall()
      session_identification.clear()
      id_number = str(returned[0])
      print(clean_data(id_number))

      return clean_data(id_number)

# residential address
def get_residential_address():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      street_address = get_street_address()
      town_city = get_town_city()
      postal_code = get_postal_code()
      session_identification.clear()
      return street_address, town_city, postal_code
'''

get_residential function broken up into 3 parts:
- get_street_address
- get_town_city
- get_postal_code

'''
# get street address
def get_street_address():
      sql_get_street_address = "select street_address from user where id =%s;"
      cursor.execute(sql_get_street_address, session_identification)
      returned = cursor.fetchall()
      street_address = str(returned[0])
      print(clean_data(street_address))

      return clean_data(street_address)
#get town city
def get_town_city():
      sql_get_town_city = "select town_city from user where id =%s;"
      cursor.execute(sql_get_town_city, session_identification)
      returned = cursor.fetchall()
      town_city = str(returned[0])
      print(clean_data(town_city))

      return clean_data(town_city)
#get postal code
def get_postal_code():
      sql_get_postal_code = "select postal_code from user where id =%s;"
      cursor.execute(sql_get_postal_code, session_identification)
      returned = cursor.fetchall()
      postal_code = str(returned[0])
      print(postal_code)

      return clean_data(postal_code)


# phone number
def get_phone_number():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_get_phone_number = "select cell_no from user where id =%s;"
      cursor.execute(sql_get_phone_number, session_identification)
      returned = cursor.fetchall()
      session_identification.clear()
      phone_number = str(returned[0])
      print(clean_data(phone_number))
      
      return clean_data(phone_number)

# email address
def get_email_address():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_get_email_address = "select email from user where id =%s;"
      cursor.execute(sql_get_email_address, session_identification)
      returned = cursor.fetchall()
      session_identification.clear()
      email_address = str(returned[0])
      print(clean_data(email_address))
      
      return clean_data(email_address)



'''

APPLICATION ROUTES

'''
# user profile
@app.route('/user_information/')
def user_profile():
      
      if session_authenticator() == True:
            logout = 'logout'
            dashboard = 'dashboard'
            username = get_username()
            surname = get_surname()
            id_number = get_id_number()
            residential_adress = get_residential_address()
            cel_number = get_phone_number()
            email_address = get_email_address()

            return render_template('information.html', logout=logout, dashboard=dashboard, username=username, surname=surname, id_number=id_number, cel_number=cel_number, email_address=email_address, residential_address=residential_adress)
      
      elif session_authenticator() == False:
            return main()
      
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
      print('user logged off')
      return main()


# application start
@app.route('/', methods = ['POST','GET'])
def main():

      if session_authenticator() == True:
            logout = 'logout'
            dashboard = 'dashboard'
            return render_template ('app.html',logout=logout,dashboard=dashboard)
      
      elif session_authenticator() == False:
             login = 'login'
             dashboard = 'dashboard'
             return render_template ('index.html',login=login)
      
      else:
            print('failed to start app')
            return('an error occured')
             
    
if __name__ == '__main__':
    app.run (debug = True)