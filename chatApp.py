from flask import Flask, render_template, request, redirect, session
import csv
import os
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

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

        #session['username']=username    
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
 if 'username' in session:

    if request.method== 'POST':
        new_room=request.form['new_room']
        if romm_is_exists(new_room):
           print("the room is already exists")
           return redirect('/lobby')   
        else:
          f= open("rooms/"+new_room +".txt","w+")
    rooms =os.listdir('rooms')    
    return render_template('lobby.html', rooms=rooms)
 else:
       return render_template('/')
    

@app.route('/chat/<room>', methods=['GET','POST'])
def chat_room(room):
      return render_template('chat.html', room=room)

# @app.route('api/chat/<room>', methods=['GET','POST'])
# def api_chat_room(room):
#   file = room
#   if request.metod == "POST":
#        msg = request.form['msg']
#        current_d_t=datetime.now()
#        with open('text_file.txt', 'a') as file:
#         file.write( current_d_t + "  :טובה לבנתיים עד שאני אקלוט מי היוזר הנוכחי"+ msg + '\n')
#         file.read()
    #  return "hhhhh"
#   return render_template('chat.html')





if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0', port='5000', debug='True')