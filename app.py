import mysql.connector
from flask import Flask, render_template, request, redirect, session
from tabulate import tabulate
from PIL import Image
import random
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'



HOST = 'localhost'
DATABASE = 'letting'
USER = 'liveserver'
PASSWORD = 'liveserver1'

'''

LIST

'''

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

      sql_statement = sql_statement
      print(sql_statement)

      data_source = data_source

      cursor.execute(sql_statement, data_source)
      db_connection.commit()
      cursor.close

# delete data from database
def delete_data(sql_statement, data_source):

      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()

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
            insert_data("insert into users (username, email, password) values (%s, %s,%s)", [username, email, password])
            set_session()
            details = username + ': registered'
            app_log(details)
            print(details)
            return main()
      else:
            print('passwords do not match')

# validates email address to verify user account existance on the database or if email address is linked to another user
def validate_email():

            email = request.form['email']

            data = clear_int(fetch_data("select exists (select email from users where email=%s);", [email]))
            
            if data == 1:
                  print(str(email) + ': address exists')
                  return True

            elif data == 0:
                  print(str(email) + ': address does not exist')
                  return False
            
            else:
                  print('Failed to run "validate_email" function')

# authenticates user username and password upon login 
def user_authentication():
      #pass login form data to variables
      username = request.form['username']
      password = request.form['password']
      # accesss database to complete user authentication
      data = clear_int(fetch_data("select exists (select * from users where username=%s and password=%s);", [username, password]))
      
      if data == 1:
            set_session()
            print('user match found')
            return True

      elif data == 0:
            print('user match not found')
            return False
      
      else:
            print('Failed to run "user_authentication()" function')

# initiates session upon successful login
def set_session():
      def fetch_count():
             # connect to database 
            db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
            cursor = db_connection.cursor()

            # sql statement to fetch requested data
            cursor.execute('select count(*) from log;')
            db_data = cursor.fetchall()
            cursor.close()

            return db_data
      
      username = request.form['username']
      password = request.form['password']
      db_data = clear_int(fetch_count())

      number = random.randint(1,1000000)

      session_id = str(db_data) + str(number)
      
      update_data('update users set session_id =%s where username =%s and password =%s', [session_id, username, password]) 
      session['id'] = session_id

      print(str(session_id) + ' session initiated')

# session authentication
def session_authenticator():

      session_id = session.get('id')

      if str(session_id) == 'None':
            print('session id not set')
            return False

      else:
            data = clear_int(fetch_data("select exists (select session_id from users where session_id =%s);", [session_id]))

            if data == 1:
                  print('session_id match found')
                  return True
            
            elif data == 0:
                  print('session_id match not found')
                  return False
            
            else:
                  print('Failed to run "session_authenticator()" function')
# application log
def app_log(details):
      if session_authenticator() == True:
            user_id = clear_int(fetch_data('select id from users where session_id=%s', [session_id]))
            details = details
            insert_data('insert into log (user_id, details) values (%s, %s)', [user_id, details])
      elif session_authenticator() == False:
            user_id = 'Guest'
            details = details
            insert_data('insert into log (user_id, details) values (%s, %s)', [user_id, details])
      print( str(user_id) + str(details))

'''

get_residential function broken up into 3 parts:
- get_street_address
- get_town_city
- get_postal_code

'''

# pulls approved items from db

'''

APPLICATION ROUTES

'''
# user profile
@app.route('/user_information/')
def user_profile():
      
      if session_authenticator() == True:
            session_id = session.get('id')
            usr_data = fetch_data('select user_icon, username, surname, email, cell_no, postal_code, street_address, town_city from users where session_id= %s;',[session_id] )
            #usr_icon = fetch_data('select user_icon from users where session_id=%s', session_id)

            return render_template('information.html', usr_data=usr_data, )
      
      elif session_authenticator() == False:
            return main()

      else:
            print('Failed to run "user_proile()" function')
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
                       
            session_id = session.get('id')
            usr_data = fetch_data('select user_icon from users where session_id=%s', [session_id]) 
            user_id = clear_int(fetch_data('select id from users where session_id = %s', [session_id]))
            
            
            # pending items
            pending_img = fetch_data('select image from listings where user_id=%s and status="pending"', [user_id])
            # approved items
            approved_img = fetch_data('select image from listings where user_id=%s and status="approved"', [user_id])
            # denied items
            denied_img = fetch_data('select image from listings where user_id=%s and status="denied"', [user_id])
            return render_template('dashboard.html', usr_data=usr_data, pending_img=pending_img, approved_img=approved_img, denied_img=denied_img)

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
            user_id = clear_int(fetch_data('select id from users where session_id=%s;', [session_id]))
            

            item_name = request.form['item_name'].replace(" ","_")
            description = request.form['model_description'].replace(" ","_")
            price = request.form['price']

            number = random.randint(1, 1000000) + random.randint(1,1000000)

            filename = item_name + '_' + str(number) + str(len(description)) + str(len(item_name)) + '.jpg'
            path = 'static/assets/img'
            img_file = Image.open(request.files['item_img'])
            img_file.save(f'{path}/{filename}')
            
            backup_path = '/media/administrator/file storage/letting-rentals/listings'
            img_file.save(f'{backup_path}/{filename}')
            
            insert_data("insert into listings (user_id, item_name, description, image, price) values (%s, %s, %s, %s, %s)", [user_id, item_name, description, filename, price])
      
            app_log(str(item_name) + ' listed')
            print('item listed pending approval')
            return user_dashboard()
      
      else:
            return main()

# delist item
@app.route('/delete_product/', methods = ['POST', 'GET'])
def delist_item():
      product_name = request.form['product_name']
      path = 'static/assets/img/' + str(product_name)
      external_path = '/media/administrator/file storage/letting-rentals/listings/' + str(product_name)

      os.remove(path)
      os.remove(external_path)
      delete_data('delete from listings where image = %s;', [str(product_name)])
      
      return user_dashboard()


'''
 update user information
 { 
      username, surname, id number, residential address, phone number, email address 
 }
'''
# update username
@app.route('/update_username/', methods=['POST','GET'])
def update_username():
      
      username = request.form['username']
      session_id = session.get('id')

      update_data("update users set username = %s where session_id = %s", [username, session_id])

      return user_profile()
# update user surname
@app.route('/update_surname/', methods=['POST','GET'])
def update_surname():
      
      surname = request.form['surname']
      session_id = session.get('id')

      update_data("update users set surname = %s where session_id = %s", [surname, session_id])

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
      
      update_data("update users set street_address = %s, town_city = %s, postal_code = %s where session_id = %s", [street, town_city, postal_code, session_id])

      return user_profile()

# update phone number
@app.route('/update_phone/', methods=['POST','GET'])
def update_phone():
      
      phone = request.form['cel_number']
      session_id = session.get('id')

      update_data("update users set cell_no = %s where session_id = %s", [phone, session_id])

      return user_profile()
# update email address
@app.route('/update_email/', methods=['POST','GET'])
def update_email():
      
      email = request.form['email_address']
      session_id = session.get('id')

      update_data("update users set email = %s where session_id = %s", [email, session_id])

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
      print('user logged off')
      return main()

# Product information
@app.route('/product/', methods=['POST','GET'])
def product_info():
      product_name = request.form['product_name']
      print('this is product name:'+str(product_name))
      item_data = fetch_data('select item_name, verification, description, price from listings where image=%s', [product_name] )
      session_id = session.get('id')
      usr_data = fetch_data('select user_icon from users where session_id=%s', [session_id])
      ex_type = clear_str((fetch_data('select type from listings where image=%s;', [product_name])))
      print(str(ex_type))
      if ex_type == 'lease':
            return render_template('product.html', usr_data=usr_data, product_name=product_name, item_data=item_data, lease=ex_type)
      
      elif ex_type == 'purchase':
            return render_template('product.html', usr_data=usr_data, product_name=product_name, item_data=item_data, purchase=ex_type)
      
      elif ex_type == 'not specified':
            return render_template('product.html', usr_data=usr_data, product_name=product_name, item_data=item_data, error=ex_type)

# application start
@app.route('/', methods = ['POST','GET'])
def main():

      if session_authenticator() == True:

            item_data = fetch_data('select image, item_name, price from listings where status=%s', ['approved'] )
            session_id = session.get('id')
            usr_data = fetch_data('select user_icon from users where session_id=%s', [session_id])
            print('session authentication success')
            return render_template ('app.html', item_data=item_data, usr_data=usr_data)
      
      elif session_authenticator() == False:
            def get_ip():
                  ip_address = request.remote_addr
                  return f'{ip_address}'
            user_id = str(get_ip())
            details = 'interaction initiated'
            insert_data('insert into log (user_id, details) values (%s,%s)', [user_id, details])
            usr_data = [('default.jpg'),]
            print('no session exists')
            return render_template ('index.html', usr_data=usr_data)
      
      else:
            login = 'login'
            print('failed to start app: session authenticator did not return true or false')
            return render_template('index.html', login=login)

# item catagory filter 
@app.route('/enable_filter/', methods=['POST','GET'])
def filter():
      catagory = request.form['catagory']
      item_data = fetch_data('select image, item_name, price from listings where status=%s and catagory=%s', ['approved',catagory])
      session_id = session.get('id')
      usr_data = fetch_data('select user_icon from users where session_id=%s', [session_id])
      remove_filter = 'remove-filter'
      return render_template ('app.html', item_data=item_data, usr_data=usr_data, remove_filter=remove_filter)

if __name__ == '__main__':
    app.run (debug = True, host='0.0.0.0')