import random
import psycopg2
from connect import config
from datetime import datetime
import pytz
from flask import Flask, render_template
from config import host, database, user, password

### Make the flask app
app = Flask(__name__)

params = config()
conn = psycopg2.connect(**params)

cur = conn.cursor()
file = open("schema.sql", "r")
alltext = file.read()
cur.execute(alltext)
conn.commit()
cur.execute('SELECT content FROM entries WHERE id = 1')
designer = cur.fetchone()
cur.close()
conn.close()
time_now = datetime.time(datetime.now())


### Routes
@app.route("/")
def get_name():
    name = ['Valeria', 'Shvets', 'KID-21']
    final = random.choice(name)
    return render_template("name.html", final=final)


@app.route("/time")
def get_time():
    now = datetime.now().astimezone(pytz.timezone('Europe/Uzhgorod'))
    timestring = now.strftime("%Y-%m-%d %H:%M:%S")  # format the time as a easy-to-read string
    return render_template("time.html", timestring=timestring)


@app.route("/dump")
def dump_entries():
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rows = cursor.fetchall()
    output = ""
    for_row = ""
    for r in rows:
        for el in r:

            output += str(el) + " " + "\t"
        output += "\n"
    return render_template('dump.html', dump=output)


@app.route("/browse")
def browse():
     conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
)
     cursor = conn.cursor()
     cursor.execute('select id, date, title, content from entries order by date')
     rowlist = cursor.fetchall()

     return render_template('browse.html', entries=rowlist)

### Start flask
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)