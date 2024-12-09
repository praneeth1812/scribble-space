from flask import Flask, render_template, redirect, request, url_for,session
import sqlite3 as sql

app = Flask(__name__)
user = ""
app.secret_key = 'private_key'
@app.route("/login")
def login():
    if not('logged_in' in session and session['logged_in']):
        return render_template('login.html')
    else:
        return redirect(url_for('index'))
        
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        u = session['username']
        return render_template('index.html',u=u)
    else:
        return redirect(url_for('login'))
    

@app.route("/signupreg")
def registration():
    return render_template('signup.html')
@app.route("/signup",methods = ['POST','GET'])
def signup():
    if request.method == "POST":
        try:
            r_user = request.form["username"]
            r_pas = request.form["password"]
            r_email = request.form["email"]
            with sql.connect("database.db") as conn:
                curr = conn.cursor()
                curr.execute("INSERT OR REPLACE INTO auth (username,password,email) VALUES(?,?,?)",(r_user,r_pas,r_email))
                conn.commit()
        except:
            conn.rollback()
        conn.close()
    return redirect(url_for('login'))
@app.route("/verify",methods = ['POST','GET'])
def verify():
    if request.method == "POST":
        pas = ""
        try:
            global user
            user = request.form["username"]
            pas = request.form["password"]
            with sql.connect("database.db") as conn:
                curr = conn.cursor()
                curr.execute(
                    "CREATE TABLE IF NOT EXISTS auth (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL,email TEXT NOT NULL)"
                )
                conn.commit()
                curr.execute("SELECT password FROM auth WHERE username = ?",(user,))
                d_pas = curr.fetchall()
                conn.close()
        except:
            print("Error occured")
        try:
            if pas == d_pas[0][0]:
                session['logged_in'] = True
                session['username'] = user
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))
    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
