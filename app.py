from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


# Connecting to db

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'demo'

mysql = MySQL(app)


# Adding data to db, table Users
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Users(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
