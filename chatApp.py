from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homePage():
    
    return render_template('register.html')


# @app.route('/lobby')
# def 

@app.route('/login')
def loginPage():
    
    return render_template('login.html')

# @app.route('/lobby')
# def homePage():
    
#     return render_template('register.html')


if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0', debug='True')