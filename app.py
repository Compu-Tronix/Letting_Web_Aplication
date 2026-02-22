# import necessary libraries
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for
from flask_mail import Mail, Message
from tabulate import tabulate
from PIL import Image
from dotenv import load_dotenv
import json
import random
import os
# load environment variables from .env file
load_dotenv()
# initialize flask app
app = Flask(__name__)
# set secret key for flask session management
app.config['SECRET_KEY'] = os.getenv('KEY')
# set email server details for flask mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')
# initialize flask mail
mail = Mail(app)
# database connection details
USER =  'liveserver'
HOST = 'localhost'
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

# return string without special characters
def clear_str(value):
      # remove first 3 and last 4 characters from string
      del_suffix = str(value)[:-4]
      del_prefix = del_suffix[:0] + del_suffix[3:]
      str_data = del_prefix
      return str_data
# return integer without special characters
def clear_int(value):
      value = value
      string = ''
      # iterate through tuple to extract integer value
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
      # fetch requested data
      sql_statement = sql_statement
      print('executing sql statement: ' + str(sql_statement))
      data_source = data_source
      print('data source for sql statement: ' +str(sql_statement) + ': ' + str(data_source))
      cursor.execute(sql_statement, data_source)
      db_data = cursor.fetchall()
      cursor.close()
      print('data returned from database: ' + str(db_data))
      return db_data
# insert new data into database
def insert_data(sql_statement, data_source):
      # connect to database
      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()
      # insert new data
      sql_statement = sql_statement
      print('executing sql statement: ' + str(sql_statement))
      data_source = data_source
      print('data source for sql statement: ' +str(sql_statement) + ': ' + str(data_source))
      cursor.execute(sql_statement, data_source)
      db_data = cursor.fetchall()
      db_connection.commit()
      cursor.close()
      print('data inserted into database: ' + str(data_source))
      return db_data
# update user data on database
def update_data(sql_statement, data_source):
      # connect to database
      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()
      # update data
      sql_statement = sql_statement
      print('executing sql statement: ' + str(sql_statement))
      data_source = data_source
      print('data source for sql statement: ' +str(sql_statement) + ': ' + str(data_source))
      cursor.execute(sql_statement, data_source)
      db_connection.commit()
      cursor.close
      print('data updated on database: ' + str(data_source))
# delete data from database
def delete_data(sql_statement, data_source):
      # connect to database
      db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
      cursor = db_connection.cursor()
      # delete data
      sql_statement = sql_statement
      print('executing sql statement: ' + str(sql_statement))
      data_source = data_source
      print('data source for sql statement: ' +str(sql_statement) + ': ' + str(data_source))
      cursor.execute(sql_statement, data_source)
      db_connection.commit()
      cursor.close
      print('data deleted from database: ' + str(data_source))
# set user session
def set_session(session_name):
      if str(session_name) == 'id':
            # fetch count of all entries in log table
            def fetch_count():
                  # connect to database 
                  db_connection = mysql.connector.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD, auth_plugin='caching_sha2_password')
                  cursor = db_connection.cursor()
                  # fetch count of all entries in log table
                  cursor.execute('select count(*) from log;')
                  db_data = cursor.fetchall()
                  cursor.close()
                  return db_data
            # set session id to count of all entries in log table + random number between 1 and 1000000
            username = request.form['username']
            password = request.form['password']
            db_data = clear_int(fetch_count())
            number = random.randint(1,1000000)
            session_id = str(db_data) + str(number)
            update_data('update users set session_id =%s where username =%s and password =%s', [session_id, username, password]) 
            session['id'] = session_id
            print('session for user ' + str(username) + ' set to: ' + str(session_id))
      else:
            usr = session_name
            session['usr'] = usr
            print('sesssion for user')
# authenticate user session
def session_authenticator():
      # check if session id exists on database and return true if match found, false if match not found, and print error message if function fails to run
      session_id = session.get('id')
      if str(session_id) == 'None':
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
# log user actions
def app_log(details):
      # log user actions on database with user id and details of action, if no user session exists log user action with user ip address and details of action
      if session_authenticator() == True:
            session_id = session.get('id')
            user_id = clear_int(fetch_data('select id from users where session_id=%s', [session_id]))
            details = details
            insert_data('insert into log (user_id, details) values (%s, %s)', [user_id, details])
      elif session_authenticator() == False:
            user_id = 'Guest'
            details = details
            insert_data('insert into log (user_id, details) values (%s, %s)', [user_id, details])
      print( str(user_id) + str(details))
# send email to user
def send_email(mail_address, subject, mail_body):
      msg = Message(subject, recipients=[mail_address])
      msg.body = mail_body
      mail.send(msg)
      print('mail sent to ' + mail_address + ' with subject: ' + subject + ' and body: ' + mail_body)
      return main()
# app routes
# list
@app.route('/list_item/', methods = ['POST', 'GET'])
def list_item():
      if session_authenticator() == True:
            # get form data
            session_id = session.get('id')
            user_id = clear_int(fetch_data('select id from users where session_id=%s;', [session_id]))
            item_name = request.form['item_name'].replace(" ","_")
            description = request.form['model_description'].replace(" ","_")
            price = request.form['price']
            # save item image to static/assets/product_img with unique filename
            number = random.randint(1, 1000000) + random.randint(1,1000000)
            filename = item_name + '_' + str(number) + str(len(description)) + str(len(item_name)) + '.jpg'
            path = 'static/assets/product_img'
            img_file = Image.open(request.files['item_img'])
            img_file.save(f'{path}/{filename}')
            # insert item data into database and log user action
            insert_data("insert into listings (user_id, item_name, description, image, price) values (%s, %s, %s, %s, %s)", [user_id, item_name, description, filename, price])
            app_log(str(item_name) + ' listed')
            return user_dashboard()
      else:
            return main()
# delist
@app.route('/delete_product/', methods = ['POST', 'GET'])
def delist_item():
      product_name = request.form['product_name']
      path = 'static/assets/product_img/' + str(product_name)
      os.remove(path)
      delete_data('delete from listings where image = %s;', [str(product_name)])
      app_log(str(product_name) + ' delisted')
      return user_dashboard()
# update user information
@app.route('/update_user_information/', methods=['POST','GET'])
def update_user_infomation():
      if session_authenticator() == True:
            #get user data from form
            user_data_type = request.form['user_data_type']
            user_data_value = request.form['user_data_value']
            session_id = session.get('id')
            #construct sql statement to update user data
            if user_data_type == 'address':
                  street = request.form['street_value']
                  town = request.form['town_value']
                  code = request.form['code_value']
                  sql_stament = "update users set street_address=%s, town_city=%s, postal_code=%s where session_id=%s;"
                  #update user data on database
                  update_data(sql_stament, [street, town, code, session_id])
                  #log user action
                  app_log('residential address updated to ' + str(street) + ', ' + str(town) + ', ' + str(code))
                  #get user data
                  usr_data = fetch_data('select user_icon, username, surname, email, cell_no, postal_code, street_address, town_city from users where session_id= %s;',[session_id] )
                  #serialize user data to json string
                  usr_data_str = json.dumps(usr_data)
                  #redirect to dashboard
                  return redirect(url_for('dashboard_filter_enabled', catagory='information', user_data_str=usr_data_str))
            else:
                  sql_stament = "update users set " + str(user_data_type) + " = %s where session_id = %s"
                  #update user data on database
                  update_data(sql_stament, [user_data_value, session_id])
                  #log user action
                  app_log(str(user_data_type) + ' updated to ' + str(user_data_value))
                  #get user data
                  usr_data = fetch_data('select user_icon, username, surname, email, cell_no, postal_code, street_address, town_city from users where session_id= %s;',[session_id] )
                  #serialize user data to json string
                  usr_data_str = json.dumps(usr_data)
                  #redirect to dashboard
                  return redirect(url_for('dashboard_filter_enabled', catagory='information', user_data_str=usr_data_str))
      
      elif session_authenticator() == False:
            return redirect(url_for('main'))
      
      else:
            print('update_user_information function failed')
            return redirect(url_for('main'))
#new user registration
@app.route('/register/', methods=['POST', 'GET'])
def register():
      # get form data
      username = request.form['username']
      email = request.form['email']
      password = request.form['password']
      confirm_password = request.form['confirm_password']
      # check if passwords match
      if password == confirm_password:
                  # search database for existing email
                  if clear_int(fetch_data("select exists (select email from users where email=%s);", [email])) == 0:
                        insert_data("insert into users (username, email, password, user_icon) values (%s, %s,%s, %s);", [username, email, password, 'default_user_icon.png'])
                        app_log(username + ': registered')
                        return redirect(url_for('main'))
                  elif clear_int(fetch_data("select exists (select email from users where email=%s);", [email])) == 1:
                        return redirect(url_for('main'))
                  else:
                        print('register function error')
                        return redirect(url_for('main'))
      else:
            print('passwords do not match')
            return redirect(url_for('main'))
# Product information
@app.route('/product/', methods=['POST','GET'])
def product_info():
      if session_authenticator() == True:
            #get product name from form
            product_name = request.form['product_name']
            #get product data from db
            product_data = fetch_data('select item_name, verification, description, price, type from listings where image=%s', [product_name] )
            #serialize product_data to json string
            product_data_str = json.dumps(product_data)
            return redirect(url_for ('product_infomation', product_data_str=product_data_str, product_name=product_name))
      elif session_authenticator() == False:
            return main()
      else:
            print('in-app filter failed')
            return main()
#product information redirect
@app.route('/product_info/')
def product_infomation():
      product_name = request.args.get('product_name')
      product_data_str = request.args.get('product_data_str')
      #deserialize json stirng back to python list
      product_data = json.loads(product_data_str)
      #render product.html with product data
      return render_template('product.html', item_data=product_data, product_name=product_name)
#user dashboard & filters
@app.route('/enable_dashboard_filter/', methods=['POST','GET'])
def dashboard_filter():
      if session_authenticator() == True:
            #get catagory from form
            catagory = request.form.get('catagory')
            #redirect based on catagory selected
            if catagory == 'information':
                  #get user data from db
                  user_data_str = session.get('usr')
                  return redirect(url_for('dashboard_filter_enabled', catagory=catagory, user_data_str=user_data_str))
            #dashboard.html db product query with catagory filter applied
            elif catagory == 'pending' or catagory == 'activated' or catagory == 'history':
                  item_data = fetch_data('select image, item_name, price from listings where status=%s', [catagory])
                  #serialize item_data to JSON string
                  item_data_str = json.dumps(item_data)
                  return redirect(url_for('dashboard_filter_enabled', catagory=catagory, item_data_str=item_data_str))
            #app.html db product query without catagory filter applied
            elif catagory == 'catagory1' or catagory == 'catagory2' or catagory == 'catagory3':
                  product_data = fetch_data('select image, item_name, price from listings where status=%s and catagory=%s', ['approved', catagory])
                  #serialize product_data to JSON string
                  product_data_str = json.dumps(product_data)
                  return redirect(url_for('dashboard_filter_enabled', catagory=catagory, product_data_str=product_data_str)) 
            else:
                  print('dashboard_filter function failed: catagory not recognised')
                  return main() 
      elif session_authenticator() == False:
            return main()
      else:
            print('dashboard_filter function failed')
            return main()
#user dashboard & filters redirect   
@app.route('/dashboard_filter_enabled/')
def dashboard_filter_enabled():
      catagory = request.args.get('catagory')
      user_data_str = request.args.get('user_data_str')
      item_data_str = request.args.get('item_data_str')
      product_data_str = request.args.get('product_data_str')
      #deserialize JSON strings back to Python lists
      user_data = json.loads(user_data_str) if user_data_str else []
      item_data = json.loads(item_data_str) if item_data_str else []
      product_data = json.loads(product_data_str) if product_data_str else []
      #render information.html based on catagory selected
      if catagory == 'information':
            return render_template('information.html', title=catagory, user_data=user_data)
      #render dashboard.html based on catagory selected
      elif catagory == 'pending' or catagory == 'activated' or catagory == 'history':
            return render_template ('dashboard.html', title=catagory, item_data=item_data)
      #reder app.html based on catagory selected
      elif catagory == 'catagory1' or catagory == 'catagory2' or catagory == 'catagory3':
            return render_template ('app.html', title=catagory, item_data=product_data, user_data=user_data,)
      else:
            print('dashboard_filter_enabled function failed')
            return main()
# user logout
@app.route('/logout/')
def logout():
      session.clear()
      print('user logged off')
      return redirect(url_for('main'))
# user login
@app.route('/login/',methods=['POST','GET'])
def login():
      #get data from login form
      username = request.form['username']
      password = request.form['password']
      #validate user login credentials
      if clear_int(fetch_data("select exists (select * from users where username=%s and password=%s);", [username, password])) == 1:
            user_data = fetch_data('select user_icon, username, surname, email, cell_no, postal_code, street_address, town_city from users where username=%s and password=%s;',[username, password])
            user_data_str = json.dumps(user_data)
            set_session(user_data_str)
            set_session('id')
            app_log('logged in')
            return redirect(url_for('main'))
      
      elif clear_int(fetch_data("select exists (select * from users where username=%s and password=%s);", [username, password])) == 0:
            app_log('logged out')
            print('user login failed')
            return redirect(url_for('main'))

      else:
            print('login function error')
            return redirect(url_for('main'))
# application start
@app.route('/', methods = ['GET'])
def main():
      if session_authenticator() == True:
            item_data = fetch_data('select image, item_name, price from listings where status=%s', ['activated'] )
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

if __name__ == '__main__':
    app.run (debug = True, host='0.0.0.0')