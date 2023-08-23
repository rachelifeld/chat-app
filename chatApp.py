from flask import Flask, render_template, request, redirect, session, jsonify
import csv
import os
import base64
from datetime import datetime

app = Flask(__name__)

def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')


def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username:
                     return redirect("/login") 
        encode_pass=encode_password(password)        
        with open('users.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, encode_pass])


    return render_template('register.html')

def verify(username,password):
     with open('users.csv', 'r', newline='') as f: 
         reader = csv.reader(f)
         for row in reader:
                if row[0] == username and decode_password(row[1]) == password:
                    return True
     return False            



# @app.route('/lobby')
# def 

@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method== 'POST':
      username= request.form['username']
      password=request.form['password']
      if verify(username,password):
          #session['username']=username
          return redirect('/lobby')
     return render_template('login.html') 
    

   

# @app.route('/lobby')
# def homePage():
    
#     return render_template('register.html')


if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0', port='5000', debug='True')