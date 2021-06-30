# Import modules for ip pinging
import subprocess
import ipaddress
import socket
import os

#import for connecting python to MySQL
import mysql.connector
from mysql.connector import Error




devicesonline = [] #initializing list for devices that will respond to ping 
devicesoffline=[]
subnet = ipaddress.ip_network(unicode('192.168.20.0/24'), strict=False)
all_hosts= list(subnet.hosts())

for ip in all_hosts[65:72]:
    ip = str(ip)
    result = subprocess.call(["ping", "-c", "1", "-n", "-W", "2", ip])
    print (result)
    if result == 0:
        devicesonline.append(ip)
        #print(ip + " is online") 
    else:
        devicesoffline.append(ip)
        #print(ip + " is offline") 
        

res = [(val, 'online' ) for val in devicesonline]
# print (res)
# for ip in devicesonline:
    # print("IP is: ", ip) 
# command line ping
# ping -c 1 -n -W 2 xx.xxx.xx
# print(res)


#Creating server connection
# def create_db_connection(host_name, user_name, user_password, db_name):
    # connection = None
    # try:
        # connection = mysql.connector.connect(
            # host=host_name,
            # user=user_name,
            # passwd=user_password,
            # database=db_name,
        # )
        # print("MySQL Database connection successful")
    # except Error as err:
        # print("Error: ", err)

    # return connection
    
#connection = create_db_connection("localhost", "root", "","devicesinfo")


#creating DB
# def create_database(connection, query):
    # cursor = connection.cursor()
    # try:
        # cursor.execute(query)
        # print("Database created successfully")
    # except Error as err:
        # print("Error: ", err)

# create_database_query="CREATE DATABASE devicesinfo"
# create_database(connection, create_database_query)   


#create Query
# def execute_query(connection, query):
    # cursor = connection.cursor()
    # try:
        # cursor.execute(query)
        # connection.commit()
        # print("Query successful")
    # except Error as err:
        # print("Error: ", err)
        
#execute_query(connection, create_device_table) # Execute our defined query 
         
#create table       
# create_device_table = """
# CREATE TABLE alldevices (
    # devices_on_network INT PRIMARY KEY AUTO_INCREMENT,
    # ip_address INT UNSIGNED NOT NULL,
    # status VARCHAR(40) NOT NULL
    # );
   # """
################################

connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="raspi",
            database="devicesinfo",
        )

#deleting old table
try:

    cursor = connection.cursor()
    Delete_all_rows = """truncate table alldevices """
    cursor.execute(Delete_all_rows)
    connection.commit()
    print("All Record Deleted successfully ")

except mysql.connector.Error as error:
    print("Failed to Delete all records from database table: {}".format(error))
# finally:
    # if connection.is_connected():
        # cursor.close()
        # connection.close()
        # print("MySQL connection is closed")
        
#Filling Rows and columns

cursor = connection.cursor()

## defining the Query
query = "INSERT INTO alldevices (ip_address, status) VALUES (%s, %s)"


## executing the query with values
cursor.executemany(query, res)

## to make final output we have to run the 'commit()' method of the database object
connection.commit()

print(cursor.rowcount, "records inserted")



