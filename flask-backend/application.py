import flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
import mysql.connector
import credsHelp
from datetime import datetime, date, timedelta
#Andrews Import DELETE ME LATER
import bcrypt

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
@cross_origin()

# Get request to get all task from the task table
@application.route('/api/tasks', methods=['GET'])
@cross_origin()
def get_tasks():
    sql = """
        SELECT 
            t.TaskID,
            t.TaskDescription,
            t.TaskPriority,
            t.TaskStatus,
            t.TaskDueDate,
            t.TaskTime,
            t.TaskType,
            t.TaskIsReviewRequired,
            t.DateCreated,
            t.CustomerID,
            t.AssignedRepresentativeID,
            t.CreatedByRepresentativeID,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            a.FirstName AS AssignedFirstName,
            a.LastName AS AssignedLastName,
            cr.FirstName AS CreatedByFirstName,
            cr.LastName AS CreatedByLastName

            FROM Task t
            LEFT JOIN Customer c ON t.CustomerID = c.CustomerID
            LEFT JOIN Representative a ON t.AssignedRepresentativeID = a.RepresentativeID
            LEFT JOIN Representative cr ON t.CreatedByRepresentativeID = cr.RepresentativeID

        """
    cursor.execute(sql)
    rows = cursor.fetchall()

    def convert(val):
        if isinstance(val, (datetime, date, timedelta)):
            return str(val)
        return val

    # Convert non-serializable values in each dict
    result = [
        {key: convert(value) for key, value in row.items()}
        for row in rows
    ]

    return jsonify(result)

# Get API request to get a single Task
@application.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    sql = """
        SELECT 
            t.TaskID,
            t.TaskDescription,
            t.TaskPriority,
            t.TaskStatus,
            t.TaskDueDate,
            t.TaskTime,
            t.TaskType,
            t.TaskIsReviewRequired,
            t.DateCreated,
            t.CustomerID,
            t.AssignedRepresentativeID,
            t.CreatedByRepresentativeID,
            c.FirstName AS CustomerFirstName,
            c.LastName AS CustomerLastName,
            r.FirstName AS AssignedFirstName,
            r.LastName AS AssignedLastName
        FROM Task t
        LEFT JOIN Customer c ON t.CustomerID = c.CustomerID
        LEFT JOIN Representative r ON t.AssignedRepresentativeID = r.RepresentativeID
        WHERE t.TaskID = %s
    """
    cursor.execute(sql, (task_id,))
    row = cursor.fetchone()

    def convert(val):
        if isinstance(val, (datetime, date, timedelta)):
            return str(val)
        return val

    if row:
        result = {key: convert(val) for key, val in row.items()}
        return jsonify(result)
    else:
        return jsonify({'message': 'Task not found'}), 404
    
from flask import request

# Post API Call to add a Task
@application.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Task (
            CustomerID, AssignedRepresentativeID, CreatedByRepresentativeID,
            CustomerName, DateCreated, TaskType, TaskIsReviewRequired,
            TaskDueDate, TaskTime, TaskPriority, TaskStatus, TaskDescription
        )
        VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data['CustomerID'],
        data['AssignedRepresentativeID'],
        data['CreatedByRepresentativeID'],
        data['CustomerName'],
        data['TaskType'],
        data['TaskIsReviewRequired'],
        data['TaskDueDate'],
        data['TaskTime'],
        data['TaskPriority'],
        data['TaskStatus'],
        data['TaskDescription']
    )

    cursor.execute(sql, values)
    conn.commit()

    return jsonify({'message': 'Task created successfully'}), 201


# PUT API call to update a task
@application.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()

    sql = """
        UPDATE Task SET
            CustomerID = %s,
            AssignedRepresentativeID = %s,
            CreatedByRepresentativeID = %s,
            CustomerName = %s,
            TaskType = %s,
            TaskIsReviewRequired = %s,
            TaskDueDate = %s,
            TaskTime = %s,
            TaskPriority = %s,
            TaskStatus = %s,
            TaskDescription = %s
        WHERE TaskID = %s
    """
    values = (
        data['CustomerID'],
        data['AssignedRepresentativeID'],
        data['CreatedByRepresentativeID'],
        data['CustomerName'],
        data['TaskType'],
        data['TaskIsReviewRequired'],
        data['TaskDueDate'],
        data['TaskTime'],
        data['TaskPriority'],
        data['TaskStatus'],
        data['TaskDescription'],
        task_id
    )

    cursor.execute(sql, values)
    conn.commit()
    return jsonify({'message': 'Task updated successfully'})

# Delete API to delete a task
@application.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    sql = "DELETE FROM Task WHERE TaskID = %s"
    cursor.execute(sql, (task_id,))
    conn.commit()
    return jsonify({'message': 'Task deleted successfully'})


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

# API for searching customers by name (First, Middle, Last)
# This is the enhanced search endpoint for the flask backend application.py

# Replace the existing search_customers function in your application.py with this one:

@application.route('/api/customers/search', methods=['GET'])
def search_customers():
    query = request.args.get('query', '')
    search_type = request.args.get('type', 'name')  # Default to name search if not specified
    
    if not query:
        return jsonify([])

    # Add wildcards to the search pattern
    search_pattern = f"%{query}%"
    
    try:
        # Construct the SQL query based on search type
        if search_type == 'id':
            sql = """
            SELECT 
                c.CustomerID, 
                c.FirstName, 
                c.MiddleName, 
                c.LastName, 
                c.Email1, 
                c.Phone1,
                c.DateOfBirth,
                c.AgentRecordID
            FROM Customer c
            WHERE CAST(c.CustomerID AS CHAR) LIKE %s
            LIMIT 10
            """
            cursor.execute(sql, (search_pattern,))
            
        elif search_type == 'email':
            sql = """
            SELECT 
                c.CustomerID, 
                c.FirstName, 
                c.MiddleName, 
                c.LastName, 
                c.Email1, 
                c.Phone1,
                c.DateOfBirth,
                c.AgentRecordID
            FROM Customer c
            WHERE c.Email1 LIKE %s
            LIMIT 10
            """
            cursor.execute(sql, (search_pattern,))
            
        elif search_type == 'phone':
            sql = """
            SELECT 
                c.CustomerID, 
                c.FirstName, 
                c.MiddleName, 
                c.LastName, 
                c.Email1, 
                c.Phone1,
                c.AgentRecordID
            FROM Customer c
            WHERE c.Phone1 LIKE %s
            LIMIT 10
            """
            cursor.execute(sql, (search_pattern,))
            
        else:  # Default to name search
            sql = """
            SELECT 
                c.CustomerID, 
                c.FirstName, 
                c.MiddleName, 
                c.LastName, 
                c.Email1, 
                c.Phone1,
                c.DateOfBirth,
                c.AgentRecordID
            FROM Customer c
            WHERE c.FirstName LIKE %s OR c.LastName LIKE %s
            LIMIT 10
            """
            cursor.execute(sql, (search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        
        # Handle empty rows case
        if not rows:
            return jsonify([])
        
        customers = []
        for row in rows:
            # Check if keys exist before accessing them
            customer_id = row.get("CustomerID", "")
            first_name = row.get("FirstName", "")
            middle_name = row.get("MiddleName", "")
            last_name = row.get("LastName", "")
            email = row.get("Email1", "")
            phone = row.get("Phone1", "")
            dob = row.get("DateOfBirth", "")
            agent_id = row.get("AgentRecordID", "")
            
            # Handle None values
            middle_name = middle_name or ""
            
            # Format the dates
            formatted_dob = str(dob) if dob else ""

            # Create a customer object matching your data structure
            customers.append({
                "id": customer_id,
                "name": f"{first_name} {middle_name} {last_name}".strip(),
                "email": email or "",
                "phone": phone or "",
                "dob": formatted_dob,
                "agent": ""  # We'll get the agent name in a separate query if needed
            })
        
        return jsonify(customers)
        
    except Exception as e:
        # Log the error with more detail to help debugging
        print(f"Error in customer search: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return a more helpful error message
        return jsonify({"error": "An error occurred while searching for customers", "details": str(e)}), 500

# POST API for login
@application.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    sql = "SELECT UserID, Username, Password, RepresentativeID FROM Users WHERE Username = %s"
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid username or password."}), 401


    # Compare password hashes
    is_valid = bcrypt.checkpw(password.encode('utf-8'), user['Password'].encode('utf-8'))

    if not is_valid:
        return jsonify({"message": "Invalid username or password."}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["UserID"],
            "username": user["Username"],
            "representative_id": user["RepresentativeID"]
        }
    })



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


# API for adding a new customer
@application.route('/api/Customer', methods=['POST'])
def add_customer():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Create SQL query for inserting a new customer
        sql = """
        INSERT INTO Customer (
            Type, FirstName, MiddleName, LastName, Suffix, 
            Title, Salutation, ActiveStatus, Country, USAResidentStatus,
            Address, Zip, City, State, SameMailingAddress, 
            MailingCountry, MailingAddress, MailingZip, MailingCity, MailingState,
            Phone1, Phone2, Phone3, DriversLicenseNum, DriversLicenseState,
            DateOfBirth, SocialSecurityNum, Gender, MaritalStatus,
            HouseholdSize, HouseholdIncome, Email1, Email2, Website, PrefferedContact,
            DoNotEmail, DoNotText, DoNotCall, DoNotMarket, DoNotCaptureEmail,
            UndeliverableMail, BadPhone1, BadPhone2, BadPhone3, BadPhone4,
            UndeliverableEmail1, UndeliverableEmail2
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        # Prepare values for insertion
        values = (
            data.get('Type'), 
            data.get('FirstName'), 
            data.get('MiddleName'), 
            data.get('LastName'), 
            data.get('Suffix'),
            data.get('Title'), 
            data.get('Salutation'), 
            data.get('ActiveStatus'), 
            data.get('Country'), 
            data.get('USAResidentStatus'),
            data.get('Address'), 
            data.get('Zip'), 
            data.get('City'), 
            data.get('State'), 
            data.get('SameMailingAddress'),
            data.get('MailingCountry'), 
            data.get('MailingAddress'), 
            data.get('MailingZip'), 
            data.get('MailingCity'), 
            data.get('MailingState'),
            data.get('Phone1'), 
            data.get('Phone2'), 
            data.get('Phone3'),
            data.get('DriversLicenseNum'), 
            data.get('DriversLicenseState'), 
            data.get('DateOfBirth'), 
            data.get('SocialSecurityNum'), 
            data.get('Gender'), 
            data.get('MaritalStatus'),
            data.get('HouseholdSize'), 
            data.get('HouseholdIncome'),
            data.get('Email1'), 
            data.get('Email2'), 
            data.get('Website'), 
            data.get('PrefferedContact'),
            data.get('DoNotEmail'), 
            data.get('DoNotText'), 
            data.get('DoNotCall'), 
            data.get('DoNotMarket'), 
            data.get('DoNotCaptureEmail'),
            data.get('UndeliverableMail'), 
            data.get('BadPhone1'), 
            data.get('BadPhone2'), 
            data.get('BadPhone3'), 
            data.get('BadPhone4'),
            data.get('UndeliverableEmail1'), 
            data.get('UndeliverableEmail2')
        )
        
        # Execute the SQL query
        cursor.execute(sql, values)
        
        # Get the ID of the last inserted row
        customer_id = cursor.lastrowid
        
        # Commit the changes
        conn.commit()
        
        # Return the newly created customer ID
        return jsonify({
            'message': 'Customer added successfully',
            'CustomerID': customer_id
        }), 201
        
    except Exception as e:
        # Log the error
        print(f"Error adding customer: {str(e)}")
        
        # Roll back any changes if an error occurs
        conn.rollback()
        
        # Return error response
        return jsonify({
            'error': 'Failed to add customer',
            'details': str(e)
        }), 500

# API for updating a customer
@application.route('/api/Customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Create SQL query for updating an existing customer
        sql = """
        UPDATE Customer SET
            Type = %s, 
            FirstName = %s, 
            MiddleName = %s, 
            LastName = %s, 
            Suffix = %s,
            Title = %s, 
            Salutation = %s, 
            ActiveStatus = %s, 
            Country = %s, 
            IsUSACitizen = %s,
            Address = %s, 
            Zip = %s, 
            City = %s, 
            State = %s, 
            AddressVerified = %s,
            MailingCountry = %s, 
            MailingAddress = %s, 
            MailingZip = %s, 
            MailingCity = %s, 
            MailingState = %s,
            Phone1 = %s, 
            Phone2 = %s, 
            Phone3 = %s, 
            Phone4 = %s,
            DriversLicenseNum = %s, 
            DriversLicenseState = %s, 
            DateLicensed = %s,
            DateOfBirth = %s, 
            SocialSecurityNum = %s, 
            Gender = %s, 
            MaritalStatus = %s,
            HouseholdSize = %s, 
            PeopleApplying = %s, 
            HouseholdIncome = %s,
            Email1 = %s, 
            Email2 = %s, 
            Website = %s, 
            PreferredContact = %s,
            DoNotEmail = %s, 
            DoNotText = %s, 
            DoNotCall = %s, 
            DoNotMail = %s, 
            DoNotMarket = %s, 
            DoNotCaptureEmail = %s,
            UndeliverableMail = %s, 
            BadCell = %s, 
            BadPhone2 = %s, 
            BadPhone3 = %s, 
            BadPhone4 = %s,
            UndeliverableEmail1 = %s, 
            UndeliverableEmail2 = %s
        WHERE CustomerID = %s
        """
        
        # Prepare values for update
        values = (
            data.get('Type'), 
            data.get('FirstName'), 
            data.get('MiddleName'), 
            data.get('LastName'), 
            data.get('Suffix'),
            data.get('Title'), 
            data.get('Salutation'), 
            data.get('ActiveStatus'), 
            data.get('Country'), 
            data.get('IsUSACitizen'),
            data.get('Address'), 
            data.get('Zip'), 
            data.get('City'), 
            data.get('State'), 
            data.get('AddressVerified'),
            data.get('MailingCountry'), 
            data.get('MailingAddress'), 
            data.get('MailingZip'), 
            data.get('MailingCity'), 
            data.get('MailingState'),
            data.get('Phone1'), 
            data.get('Phone2'), 
            data.get('Phone3'), 
            data.get('Phone4'),
            data.get('DriversLicenseNum'), 
            data.get('DriversLicenseState'), 
            data.get('DateLicensed'),
            data.get('DateOfBirth'), 
            data.get('SocialSecurityNum'), 
            data.get('Gender'), 
            data.get('MaritalStatus'),
            data.get('HouseholdSize'), 
            data.get('PeopleApplying'), 
            data.get('HouseholdIncome'),
            data.get('Email1'), 
            data.get('Email2'), 
            data.get('Website'), 
            data.get('PreferredContact'),
            data.get('DoNotEmail'), 
            data.get('DoNotText'), 
            data.get('DoNotCall'), 
            data.get('DoNotMail'), 
            data.get('DoNotMarket'), 
            data.get('DoNotCaptureEmail'),
            data.get('UndeliverableMail'), 
            data.get('BadCell'), 
            data.get('BadPhone2'), 
            data.get('BadPhone3'), 
            data.get('BadPhone4'),
            data.get('UndeliverableEmail1'), 
            data.get('UndeliverableEmail2'),
            customer_id  # WHERE condition value
        )
        
        # Execute the SQL query
        cursor.execute(sql, values)
        
        # Commit the changes
        conn.commit()
        
        # Check if the update was successful (if any rows were affected)
        if cursor.rowcount > 0:
            return jsonify({
                'message': 'Customer updated successfully',
                'CustomerID': customer_id
            })
        else:
            return jsonify({
                'error': 'Customer not found or no changes made',
                'CustomerID': customer_id
            }), 404
            
    except Exception as e:
        # Log the error
        print(f"Error updating customer {customer_id}: {str(e)}")
        
        # Roll back any changes if an error occurs
        conn.rollback()
        
        # Return error response
        return jsonify({
            'error': 'Failed to update customer',
            'details': str(e)
        }), 500
    


@application.route('/api/customers/<int:customer_id>/policies', methods=['GET'])
def get_policies_for_customer(customer_id):
    sql = """
        SELECT 
            p.PolicyID,
            p.PolicyNumber,
            p.EffectiveDate,
            p.ExpirationDate,
            p.AdditionalInfo,
            c.CategoryName,
            co.CompanyName,
            p.Issuer
        FROM Policy p
        LEFT JOIN Category c ON p.CategoryID = c.CategoryID
        LEFT JOIN Company co ON p.CompanyID = co.CompanyID
        WHERE p.CustomerID = %s
        ORDER BY p.EffectiveDate DESC
    """
    cursor.execute(sql, (customer_id,))
    rows = cursor.fetchall()

    def convert(val):
        if isinstance(val, (datetime, date, timedelta)):
            return str(val)
        return val

    return jsonify([{k: convert(v) for k, v in row.items()} for row in rows])



if __name__ == "__main__":
    application.run(debug=True, threaded=True)