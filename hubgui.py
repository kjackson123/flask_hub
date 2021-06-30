# regular flask iimports
from flask import Flask, render_template, url_for, flash, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from forms import EnterIPForm


from flaskext.mysql import MySQL

import subprocess
import ipaddress
import socket
import os

# import for connecting python to MySQL
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)


@app.route("/index", methods=['GET', 'POST'])
def index():
    # PINGSCRIPT
    devicesonline = []  # initializing list for devices that will respond to ping
    devicesoffline = []
    subnet = ipaddress.ip_network(('192.168.20.0/24'), strict=False)
    all_hosts = list(subnet.hosts())
    for ip in all_hosts[70:75]:
        print(ip)
        ip = str(ip)
        result = subprocess.Popen(['ping', '-n', '1', '-w', '500', ip])
        print(result)
        if result == 0:
            devicesonline.append(ip)
            #print(ip + " is online")
        else:
            devicesoffline.append(ip)
            #print(ip + " is offline")
    # print(devicesonline)
    res = [(val, 'online') for val in devicesonline]
    # print(res)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="raspi",
        database="devicesinfo",
    )
    # deleting old table
    try:
        cursor = connection.cursor()
        Delete_all_rows = """truncate table alldevices """
        cursor.execute(Delete_all_rows)
        connection.commit()
        #print("All Record Deleted successfully ")

    except connection.Error as error:
        print("Failed to Delete all records from database table: {}".format(error))

    cursor = connection.cursor()

    # defining the Query
    query = "INSERT INTO alldevices (ip_address, status) VALUES (%s, %s)"

    # executing the query with values
    cursor.executemany(query, res)

    # to make final output we have to run the 'commit()' method of the database object
    connection.commit()

    #print(cursor.rowcount, "records inserted")

    # execute select statement to fetch data to be displayed in combo/dropdown
    cursor.execute('SELECT ip_address,status FROM alldevices')

    # fetch all rows ans store as a set of tuples
    devicelist = cursor.fetchall()
    # render template and send the set of tuples to the HTML file for displaying
    return render_template("inputTEST.html", devicelist=devicelist)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/quickstart")
def quickstart():
    return render_template('quickstart.html')


@app.route("/enterIPForm", methods=['GET', 'POST'])
def enterIP():
    '''if request.method== "POST":
        address = request.form['nm']
        return redirect(url_for("user", usr=user))
    else:'''
    form = EnterIPForm()
    return render_template('enterIP.html', title='Start Here', form=form)


'''@app.route("/<usr>")
def user(usr):
        return f"<h1>{usr}</h1>"'''


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
