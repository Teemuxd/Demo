from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'demo2'

mysql = MySQL(app)

# Register function, tests if account already exists in database and all form must be filled
@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
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

if __name__ == '__main__':
    app.run()

