from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def homePage():
   
    



    return render_template('register.html')


# @app.route('/lobby')
# def 

@app.route('/login')
def loginPage():
     if request.method== 'POST':
      username= request.form['username']
      password=request.form['password']
    

     return render_template('login.html')

# @app.route('/lobby')
# def homePage():
    
#     return render_template('register.html')


if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0', port='5000', debug='True')