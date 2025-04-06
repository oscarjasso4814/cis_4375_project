import flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import mysql.connector
import credsHelp

from mysql.connector import Error
from sqlHelp import create_connection
from sqlHelp import execute_query
from sqlHelp import execute_read_query

# Creating a connection to mysql database
myCreds = credsHelp.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
cursor = conn.cursor(dictionary=True, buffered=True)

cors = CORS()


# Setting up an application name
application = flask.Flask(__name__) #sets up the application
application.config["DEBUG"] = True #allow to show errors in browser
cors.init_app(application)

# GET API for getting a representative's name
@application.route('/api/rep/<repid>/name', methods=['GET'])
def get_rep_name(repid):
    # Retrieves representative data
    sql = "SELECT * FROM Representative WHERE RepresentativeID = " + repid;
    # Runs and commits the data insertion
    cursor.execute(sql)
    representative = cursor.fetchall()
    return jsonify(representative)

# GET API for getting a customer's profile
@application.route('/api/customer/<custid>', methods=['GET'])
def get_customer(custid):
    # Formats data into sql select command
    sql = "SELECT * FROM Customer WHERE CustomerID = " + custid;
    # Runs and commits the data insertion
    cursor.execute(sql)
    customer = cursor.fetchall()
    return jsonify(customer)

# API for searching customers by name (First, Middle, Last) WIP!
@application.route('/api/customers/search', methods=['GET'])
def search_customers():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    sql = """
    SELECT CustomerID, FirstName, MiddleName, LastName, Email1, Phone1
    FROM Customer
    WHERE 
        FirstName LIKE %s OR 
        LastName LIKE %s OR 
        MiddleName LIKE %s OR 
        Email1 LIKE %s OR 
        Phone1 LIKE %s OR 
        CustomerID LIKE %s
    LIMIT 10
    """
    cursor.execute(sql, (
        f"%{query}%", f"%{query}%", f"%{query}%",
        f"%{query}%", f"%{query}%", f"%{query}%"
    ))
    rows = cursor.fetchall()

    customers = [
        {
        "id": row["CustomerID"],
        "name": f"{row['FirstName']} {row['MiddleName'] or ''} {row['LastName']}".strip(),
        "email": row["Email1"],
        "phone": row["Phone1"]
        }
        for row in rows
    ]
    return jsonify(customers)

# API BRAINSTORMING; NOT FINAL

# GET API for getting a table
@application.route('/api/<table>', methods=['GET'])
def get_data_all(table):
    # Formats data into sql select command
    sql = f"SELECT * FROM {table}";
    # Runs and commits the data insertion
    cursor.execute(sql)
    tabledata = cursor.fetchall()
    return jsonify(tabledata)

# GET API for getting a table entry
@application.route('/api/<table>/<tableid>', methods=['GET'])
def get_data(table, tableid):
    # Retrieves data
    request_data = request.get_json()
    # Formats data into sql select command
    sql = f"SELECT * FROM {table} WHERE {table}ID = {tableid}";
    # Runs and commits the data insertion
    cursor.execute(sql)
    tabledata = cursor.fetchall()
    return jsonify(tabledata)

# GET API for getting 

# PUT API for updating a table entry; expects JSON body
@application.route('/api/<table>/<tableid>', methods=['POST'])
def post_data(table, tableid):
    # Retrieves request data
    request_data = request.get_json()
    # compiles the key: value pairs from request data
    for (key, value) in request_data.items():
        # Skips the ID key value pair and null values
        if key == 'id' or value == None:
            continue
        
        # Concatenates string values with quotations for mySQL command
        if type(value) is str:
            value = '"' + value + '"'

        # Concatenates the keys for the insert command
        if (not firstLoop):
            updates = f'{updates}, {key}={value}'
        else:
            updates = f'{key}={value}'
            firstLoop = False
    # Formats key: value data into sql update
    sql = f"UPDATE {table} SET {updates} WHERE {table}ID={tableid}";
    # Runs and commits the data insertion
    cursor.execute(sql)
    return "PUT Request Successful"

# PUT API for updating a table entry; expects JSON body with ID as a value
@application.route('/api/<table>', methods=['PUT'])
def post_data_no_id(table):
    # Retrieves request data
    request_data = request.get_json()
    tableid = request_data.id

    # strings to hold the parameters for the update statement
    firstLoop = False
    updates = ""
    for (key, value) in request_data.items():
        # Skips the ID key value pair and null values
        if key == 'id' or value == None:
            continue

        # Concatenates string values with quotations for mySQL command
        if type(value) is str:
            value = '"' + value + '"'

        # Concatenates the keys for the insert command
        if (not firstLoop):
            updates = f'{updates}, {key}={value}'
        else:
            updates = f'{key}={value}'
            firstLoop = False
    # Formats key: value data into sql update
    sql = f"UPDATE {table} SET {updates} WHERE {table}ID={tableid}";
    cursor.execute(sql)
    return "PUT Request Successful"

# DELETE API for removing a table entry
@application.route('/api/<table>/<tableid>', methods=['DELETE'])
def delete_data(table, tableid):
    # Formats data into sql delete command
    sql = f"DELETE FROM {table} WHERE {table}ID = {tableid}";
    # Runs and commits the data insertion
    cursor.execute(sql)
    return "DELETE Request Sucessful"

# POST API for adding a table entry
@application.route('/api/<table>', methods=['POST'])
def add_data(table):
    # Retrieves posted json and extracts data by keys
    request_data = request.get_json()

    # strings to hold the parameters for the insert statement
    firstLoop = False
    keys = ""
    values = ""
    for (key, value) in request_data.items():
        # Concatenates string values with quotations for mySQL command
        if type(value) is str:
            value = '"' + value + '"'

        # Concatenates the keys for the insert command
        if (not firstLoop):
            keys = f'{keys}, key'
            values = f'{values}, value'
        else:
            keys = key
            values = value
            firstLoop = False
        
    # Posting functionality
    # Formats data into sql insert command
    sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
    # Runs and commits the data insertion
    cursor.execute(sql)
    conn.commit()
    return "Post Request Successful"

if __name__ == "__main__":
    application.run()