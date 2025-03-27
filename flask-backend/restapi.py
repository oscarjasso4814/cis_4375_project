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
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser
cors.init_app(app)

# GET API for getting a representative's name
@app.route('/api/rep/<repid>/name', methods=['GET'])
def get_rep_name(repid):
    # Retrieves representative data
    sql = "SELECT * FROM Representative WHERE RepresentativeID = " + repid;
    cursor.execute(sql)
    representative = cursor.fetchall()
    return jsonify(representative)

# API for searching customers by name (First, Middle, Last) WIP!
@app.route('/api/customers/search', methods=['GET'])
def search_customers():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    sql = """
        SELECT CustomerID, FirstName, MiddleName, LastName
        FROM Customer
        WHERE FirstName LIKE %s OR MiddleName LIKE %s OR LastName LIKE %s
        LIMIT 10
    """
    cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()

    customers = [
        {
            "id": row["CustomerID"],
            "name": f"{row['FirstName']} {row['MiddleName']} {row['LastName']}".strip()
        }
        for row in rows
    ]
    return jsonify(customers)

    
app.run()