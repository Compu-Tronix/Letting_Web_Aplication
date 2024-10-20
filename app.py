import mysql.connector
from flask import Flask, render_template, request, redirect, session
from tabulate import tabulate
from PIL import Image
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'



HOST = '192.168.0.103'
DATABASE = 'letting_app'
USER = 'letting.app'
PASSWORD = 'letting@database'

'''

LISTS

'''
# registration list
reg_details = []

# user details list
user_details = []

# session identification list
session_identification = []

# update user information
user_info_update = []

listing = []

application_data = []

'''

FUNCTIONS

'''
# clears special characters from strings pulled from database
def clear_str(value):
      x = str(value)

      del_suffix = x[:-4]
      del_prefix = del_suffix[:0] + del_suffix[3:]
      str_data = del_prefix

      return str_data

# clears special characters from integers pulled from database
def clear_int(value):
      value = value
      string = ''

      for item in value:
            string = string + str(item)

            del_suffix = string[:-2]
            del_prefix = del_suffix[1:]
            data = del_prefix

            return int(data)
      

# fecth data from database
def fetch_data(sql_statement, data_source):

      # connect to database 
      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()

      # sql statement to fetch requested data
      sql_statement = sql_statement
      print(sql_statement)

      # requested data 
      data_source = data_source
      print(data_source)

      cursor.execute(sql_statement, data_source)
      db_data = cursor.fetchall()
      cursor.close()

      print(db_data)
      return db_data

# insert new data into database
def insert_data(sql_statement, data_source):
      
      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()
      print('connected to: ' + str(db_connection.get_server_info()))

      sql_statement = sql_statement
      print(sql_statement)

      data_source = data_source

      cursor.execute(sql_statement, data_source)
      db_data = cursor.fetchall()

      db_connection.commit()
      cursor.close()
      return db_data

# update user data on database
def update_data(sql_statement, data_source):

      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()
      print('connected to: ' + str(db_connection.get_server_info()))

      sql_statement = sql_statement
      print(sql_statement)

      data_source = data_source

      cursor.execute(sql_statement, data_source)
      db_connection.commit()
      cursor.close

# register new users
def user_registratoin():
      
      # pass user registation form data to variables
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
      confirm_password = request.form['confirm_password']
      
      # validate password entry to confirm user account registration
      if password == confirm_password:
            reg_details.append(username)
            reg_details.append(email)
            reg_details.append(password)
            print(username + email + password + ' appended to reg_details')

            sql_statement = "insert into users (username, email, password) values (%s, %s,%s)"
            data_source = reg_details
            insert_data(sql_statement, data_source)

            reg_details.clear()
            print(username + 'new user redistered')

      else:
            reg_details.clear()
            print('passwords do not match')

# validates email address to verify user account existance on the database or if email address is linked to another user
def validate_email():

            email = request.form['email']
            reg_details.append(email)
            print(email + 'appened to reg_details')

            sql_statement = "select exists (select email from users where email=%s);"
            data_source = reg_details                        
            db_data = fetch_data(sql_statement, data_source)
            data = clear_int(db_data)

            if data == 1:
                  print('email adress already exists')
                  reg_details.clear()
                  return True

            elif data == 0:
                  print('email address does not exist')
                  reg_details.clear()
                  return False
            
            else:
                  print('validate email function error')

# authenticates user username and password upon login 
def user_authentication():

      #pass login form data to variables
    username = request.form['username']
    password = request.form['password']
    user_details.append(username)
    user_details.append(password)
    
    # accesss database to complete user authentication
    sql_statement = "select exists (select * from users where username=%s and password=%s);"
    data_source = user_details
    db_data = fetch_data(sql_statement, data_source)
    data = clear_int(db_data)
    

    if data == 1:
      set_session()
      user_details.clear()
      print('user match found')
      return True

    elif data == 0:
      user_details.clear()
      print('user match not found')
      return False
    
    else:
         print('user_authentication function error')

# initiates session upon successful login
def set_session():
      def fetch_count():
             # connect to database 
            db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
            cursor = db_connection.cursor()

            # sql statement to fetch requested data
            sql_statement = 'select count(*) from log;'
            print(sql_statement)

            cursor.execute(sql_statement)
            db_data = cursor.fetchall()
            cursor.close()

            print(db_data)
            return db_data
      
      username = request.form['username']
      password = request.form['password']
      db_data = fetch_count()
      log = clear_int(db_data)

      number = random.randint(1,1000000)

      session_id = str(log) + str(number)
      session_identification.append(int(session_id))
      session_identification.append(username)
      session_identification.append(password)
      
      update_data('update users set session_id =%s where username =%s and password =%s', session_identification) 
      session['id'] = session_id
      session_identification.clear()

      print(str(session_id) + ' session initiated')

# session authentication
def session_authenticator():

      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + ' appended to session_identification list')

      if str(session_id) == 'None':
            print('no session id')
            session_identification.clear()
            return False

      else:
            sql_statement = "select exists (select session_id from users where session_id =%s);"
            data_source = session_identification
            db_data = fetch_data(sql_statement, data_source)
            data = clear_int(db_data)

            if data == 1:
                  print('session match found')
                  session_identification.clear()
                  return True
            
            elif data == 0:
                  print('session match not found')
                  session_identification.clear()
                  return False

# application log
def app_log(details):
      
      session_id = session.get('id')
      session_identification.append(session_id)
      user_id = clear_int(fetch_data('select id from users where session_id=%s', session_identification))

      details = details
      application_data.append(user_id)
      application_data.append(details)

      sql_statement = 'insert into log (user_id, details) values (%s, %s)'
      insert_data(sql_statement, application_data)

      application_data.clear()
      session_identification.clear()
      
      print( str(user_id) + str(details))

# pulls user username from database
def get_username():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select username from users where id =%s;"
      data_source = session_identification
     
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
     
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data

# pulls  user surname from database 
def get_surname():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select surname from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data
# updates user surname in database
def update_surname():
      print('running update_surname function')

# pulls user id number from database
def get_id_number():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select id_no from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data

'''

get_residential function broken up into 3 parts:
- get_street_address
- get_town_city
- get_postal_code

'''
def get_residential_address():
      street_address = get_street_address()
      town_city = get_town_city()
      postal_code = get_postal_code()

      return street_address, town_city, postal_code
# pulls users street address from database
def get_street_address():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select street_address from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data
# pulls users town city from database
def get_town_city():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select town_city from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data
# pulls users postal code from database
def get_postal_code():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select postal_code from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data

# pulls users phone number from database
def get_phone_number():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select cell_no from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data

# pulls users email address from database
def get_email_address():
      session_id = session.get('id')
      session_identification.append(session_id)
      print(str(session_id) + 'appended to session_identification list')

      sql_statement = "select email from users where id =%s;"
      data_source = session_identification
      
      db_data = fetch_data(sql_statement, data_source)
      data = clear_str(db_data)
      
      session_identification.clear()

      if data == 'on':
            print(data)
            return  'none'

      else:
            print(data)
            return data

# pulls approved items from db

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



'''
user dashboard
{
list new item, item history, listed items, pending items
}
'''
@app.route('/dashboard/', methods=['POST','GET'])
def user_dashboard():

      if session_authenticator() == True:
            
            logout = 'Logout'
            dashboard = 'Dashboard'
            
            session_identification.append(session.get('id'))
            data_source = session_identification
            

            
            db_data = fetch_data('select id from users where session_id = %s', data_source)
            user_id = clear_int(db_data)
            
            
            
            application_data.append(user_id)
            session_identification.clear()
            # pending items
            pending_img = fetch_data('select image from listings where item_id=%s and status="pending"', application_data)
            # approved items
            approved_img = fetch_data('select image from listings where item_id=%s and status="approved"', application_data)
            
            application_data.clear()

            return render_template('dashboard.html', logout=logout, dashboard=dashboard, pending_img = pending_img, approved_img=approved_img)

      elif session_authenticator() == False:
            return main()
      
      else:
            print('user dashbord function failed')
            return main()

# upload listing item 
@app.route('/list_item/', methods = ['POST', 'GET'])
def list_item():

      if session_authenticator() == True:
            session_id = session.get('id')
            application_data.append(session_id)
            item_id = clear_int(fetch_data('select id from users where session_id=%s;', application_data))
            application_data.clear()

            item_name = request.form['item_name'].replace(" ","_")
            description = request.form['model_description'].replace(" ","_")
            price = request.form['price']

            listing.append(item_id)
            listing.append(item_name)
            listing.append(description)

            number = random.randint(1, 1000000) + random.randint(1,1000000)

            filename = item_name + '_' + str(number) + str(len(description)) + str(len(item_name)) + '.jpg'
            path = 'static/assets/img'
            img_file = Image.open(request.files['item_img'])
            img = img_file.save(f'{path}/{filename}')
            
            backup_path = '/media/administrator/file storage/letting-rentals/listings'
            backup = img_file.save(f'{backup_path}/{filename}')
            
            listing.append(filename)
            listing.append(price)

            sql_statement = "insert into listings (item_id, item_name, description, image, price) values (%s, %s, %s, %s, %s)"
            data_source = listing
            
            insert_data(sql_statement, data_source)
            
            listing.clear()

            app_log('listed item')
            print('item listed pending approval')
            return user_dashboard()
      
      else:
            return main()


'''
 update user information
 { 
      username, surname, id number, residential address, phone number, email address 
 }
'''
# update username
@app.route('/update/', methods=['POST','GET'])
def update_username():
      
      username = request.form['username']
      session_id = session.get('id')
      user_info_update.append(username)
      user_info_update.append(session_id)

      sql_statement = "update users set username = %s where id = %s"
      data_source = user_info_update

      update_data(sql_statement, data_source)
      user_info_update.clear()

      return user_profile()
# update user surname
@app.route('/update_surname/', methods=['POST','GET'])
def update_surname():
      
      surname = request.form['surname']
      session_id = session.get('id')
      user_info_update.append(surname)
      user_info_update.append(session_id)

      sql_statement = "update users set surname = %s where id = %s"
      data_source = user_info_update

      update_data(sql_statement, data_source)
      user_info_update.clear()

      return user_profile()
# update residential address
@app.route('/update_residential_address/', methods=['POST','GET'])
def update_residental_address():
      
      street = request.form['street_address']
      town_city = request.form['town_city']
      postal_code = request.form['postal_code']
      session_id = session.get('id')

      name = str(session_id) + '.jpg'
      path = 'assets/user_assets/proof_of_residence/'

      img = Image.open(request.files['proof_of_residence'])
      img = img.save(f'{path}/{name}')

      user_info_update.append(street)
      user_info_update.append(town_city)
      user_info_update.append(postal_code)
      user_info_update.append(path + name)
      user_info_update.append(session_id)
      
      sql_statement = "update users set street_address = %s, town_city = %s, postal_code = %s, proof_of_residence = %s where id = %s"
      data_source = user_info_update

      update_data(sql_statement, data_source)
      user_info_update.clear()

      return user_profile()
# update id number
@app.route('/update_id_number/', methods=['POST', 'GET'])
def update_id_number():

      id_number = request.form['id_number']
      session_id = session.get('id')

      name = str(session_id) + '.jpg'
      path = 'assets/user_assets/id_copies/'

      img = Image.open(request.files['id_img'])
      img = img.save(f'{path}/{name}')

      user_info_update.append(id_number)
      user_info_update.append(path + name)
      user_info_update.append(session_id)

      sql_statement = "update users set id_no = %s, id_img = %s where id = %s"
      data_source = user_info_update

      update_data(sql_statement, data_source)
      user_info_update.clear()

      return user_profile()

# update phone number
@app.route('/update_phone/', methods=['POST','GET'])
def update_phone():
      
      phone = request.form['cel_number']
      session_id = session.get('id')
      user_info_update.append(phone)
      user_info_update.append(session_id)

      sql_statement = "update users set cell_no = %s where id = %s"
      data_source = user_info_update

      update_data(sql_statement, data_source)
      user_info_update.clear()

      return user_profile()
# update email address
@app.route('/update_email/', methods=['POST','GET'])
def update_email():
      
      email = request.form['email_address']
      session_id = session.get('id')
      user_info_update.append(email)
      user_info_update.append(session_id)

      sql_statement = "update users set email = %s where id = %s"
      data_source = user_info_update

      update_data(sql_statement, data_source)
      user_info_update.clear()

      return user_profile()

# user registration
@app.route('/register/', methods=['POST', 'GET'])
def register():
            
            if request.method == 'POST':
                  
                  if validate_email() == True:
                        print('email address belongs to a user that already exsits')
                        return main()

                  elif validate_email() == False:
                        user_registratoin()
                        return main()
                  
                  else:
                        print('register function error')

# user login
@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        
        if user_authentication() == True:
            app_log('logged in')
            return main()
        
        elif user_authentication() == False:
            app_log('logged out')
            print('user login failed')
            return logout()

        else:
              print('login function error')
              return main()

# user logout
@app.route('/logout/')
def logout():
      session.clear()
      reg_details.clear()
      user_details.clear()
      session_identification.clear()
      print('user logged off')
      return main()

  



# application start
@app.route('/', methods = ['POST','GET'])
def main():

      

      if session_authenticator() == True:
            
            logout = 'logout'
            dashboard = 'dashboard'
            print('session authentication success')
            approved_img_sql_statement = 'select image from listings where status=%s'
            data_source = ['approved']
            approved_img = fetch_data(approved_img_sql_statement, data_source)

            return render_template ('app.html',logout=logout,dashboard=dashboard, approved_img=approved_img)
      
      elif session_authenticator() == False:
            def get_ip():
                  ip_address = request.remote_addr
                  return f'{ip_address}'

            details = str(get_ip()) + ' ran application'
            application_data.append(details)
            sql_statement = 'insert into log (details) values (%s)'
            insert_data(sql_statement, application_data)
            application_data.clear()
            
            login = 'login'
            print('no session exists')
            return render_template ('index.html',login=login)
      
      else:
            login = 'login'
            print('failed to start app: session authenticator did not return true or false')
            return render_template('index.html', login=login)
             
    
if __name__ == '__main__':
    app.run (debug = True, host='0.0.0.0')