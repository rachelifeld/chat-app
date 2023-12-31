from flask import Flask, render_template, request, redirect, session, jsonify
import csv
import os
import base64
from datetime import datetime


app = Flask(__name__)
app.secret_key = '1234' 
# app.config['SESSION_COOKIE_SECURE'] = False 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

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

        session['username']=username    
        return redirect("/lobby") 

    return render_template('register.html')

def verify(username,password):
     with open('users.csv', 'r', newline='') as f: 
         reader = csv.reader(f)
         for row in reader:
                if row[0] == username and decode_password(row[1]) == password:
                    return True
     return False            


@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method== 'POST':
      username= request.form['username']
      password=request.form['password']
      if verify(username,password):
          session['username']=username
          return redirect('/lobby')
     return render_template('login.html') 
    

def room_is_exists(new_room):
    if os.path.exists(new_room +".txt"):
       return True
    return False

@app.route('/lobby', methods=['GET','POST'])
def lobby():
 if session.get('username'):
    if request.method== 'POST':
        new_room=request.form['new_room']
        if room_is_exists(new_room):
           print("the room is already exists")
           return redirect('/lobby')   
        else:
          f= open("rooms/"+new_room +".txt","w+")
    rooms =os.listdir('rooms')    
    for i in range(len(rooms)):
      rooms[i] = rooms[i][:-4]
    return render_template('lobby.html', rooms=rooms)
 else:
        return redirect('/')
 
    
@app.route('/api/chat/<room>', methods=['GET', 'POST'])
def render_chat(room):
    path=os.getenv('ROOMS_FILES_PATH')+room+".txt"
    if request.method == "POST":
        msg = request.form['msg']
        current_user = session['username']
        current_d_t = datetime.now()
        with open(path, "a") as file:
            file.write(f'[{current_d_t:%Y-%m-%d %H:%M:%S}] {current_user}: {msg}\n')
    with open(path, "r") as file:
        file.seek(0)
        lines = file.read()
    return lines


@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        return render_template('chat.html', room=room)
    else:
        return redirect('/')


@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200

@app.route('/api/chat/<room>/clear', methods=['GET','POST'])
def clearPage(room):
    username= session['username']
    path=os.getenv('ROOMS_FILES_PATH')+room+".txt"
    with open(path, 'r') as f:
        lines = f.readlines()

    with open(path, 'w') as f:
        for line in lines:
            if username not in line:
                f.write(line) 
    return render_template('chat.html', room=room)



if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0', port='5000', debug='True')