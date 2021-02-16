from flask import Flask, render_template, url_for, session, request
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)
app.secret_key = 'random_stringu'
#database connection
app.config['MYSQL_HOST'] = 'eu-cdbr-west-03.cleardb.net'
app.config['MYSQL_USER'] = 'b85d3c3102119e'
app.config['MYSQL_PASSWORD'] = 'bfebaa95'
app.config['MYSQL_DB'] = 'heroku_ad0542da6c5db3f'

mysql = MySQL(app)


@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Register function, tests if account already exists in database and all form must be filled
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists'
        elif not username or not password or not email:
            msg = 'All forms must be filled'
        else:
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'Registered successfully '
    elif request.method == 'POST':
        msg = 'All forms must be filled'
    return render_template('register.html', msg=msg)


@app.route('/login', methods =['GET', 'POST']) 
def login():
    #stores data to session if login is success
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)
    
 
@app.route('/logout') 
def logout():
    #delete the session information when logging out   
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return render_template('login.html') 

if __name__ == '__main__':
    app.run()



