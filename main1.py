from flask import Flask
from flask import render_template, request, redirect, abort
import psycopg2
from psycopg2 import OperationalError


def connection(name, user, password, host, port):
    conn = None
    try:
        conn = psycopg2.connect(
            database=name,
            user=user,
            password=password,
            host=host,
            port=port,
            )
        print('Connected to database')
    except OperationalError:
        print('an operating error has occurred')
    return conn

conn = connection('phonebook', 'postgres', '1br3485a', '127.0.0.1', '5432')

def insert(name, surname, city, phone_number):
    insert = (f"INSERT INTO users (name, surname, city, phone_number) "
              f"VALUES ('{name}', '{surname}', '{city}', '{phone_number}')")
    cursor = conn.cursor()
    cursor.execute(insert)
    conn.commit()

def listing():
    cursor = conn.cursor()
    result = None
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    listing = []
    for user in result:
        listing.append(
            {'username': user[0] + user[1], 'name': user[0], 'surname': user[1], 'city': user[2], 'phone_number': user[3],
             'id': user[4]})

    return listing

app = Flask(__name__)

@app.route('/', methods=['get'])
def index():
    return redirect('http://127.0.0.1:5000/users')

@app.route('/users', methods=['get', 'post'])
def users():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        city = request.form.get('city')
        phone_number = request.form.get('phone_number')
        insert(name, surname, city, phone_number)
    return render_template('users.html', users=listing())

@app.route('/users/<username>')
def check(username):
    users = ''
    flag = []
    for i in listing():
        if username != i['username']:
            flag.append(False)
        else:
            flag.append(True)
    if any(flag) == False:
        abort(404)
    for i in listing():
        if username == i['username']:
            users = i
    return f'<h2>UserName:{users["username"]} </h2> <br>'\
           f'<h2>Name:{users["name"]} </h2> <br>'\
           f'<h2> Surname:{users["surname"]} </h2> <br>' \
           f'<h2>City:{users["city"]} </h2> <br>' \
           f'<h2>Phone_number:{users["phone_number"]} </h2> <br>'\

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_student(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    return redirect('http://127.0.0.1:5000/users')

if __name__ == '__main__':
    app.run(debug=True)