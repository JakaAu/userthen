from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "key"

my_DB = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    password = "Qlzgh2497!",
    database = "mydatabase")

mycursor = my_DB.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

wsgi_app = app.wsgi_app


@app.route('/')
def home():
    if "username" in session:
        return render_template("index.html", user = session["username"], list = list)
    else:
        return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        sql = "SELECT username FROM users WHERE username=%s AND password=%s"
        values = [username, password]
        mycursor.execute(sql,values)
        myresults = mycursor.fetchall()
        if len(myresults) > 0:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', message="Wrong username or password")
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password') 
        confirm_password = request.form.get('confirm-password') 

        if password != confirm_password:
            return render_template('register.html', message="passwords dont match")
        sql = "SELECT username FROM users WHERE username=%s"
        value = (username,)
        mycursor.execute(sql, value)
        myresult = mycursor.fetchall()
        
        if len(myresult) > 0:
            return render_template('register.html', message="username taken")
        else:
            sql = "INSERT INTO users(username, password) VALUES(%s, %s)"
            values = [username, password]
            mycursor.execute(sql, values)
            my_DB.commit()
            session["username"] = username
            return redirect("/")
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('register.html')



if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
