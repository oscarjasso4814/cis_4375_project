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

# GET API for getting an agent's notes
@application.route('/api/agentnote/<repid>', methods=['GET'])
def get_agent_notes(repid):
    # Formats data into sql select command
    sql = f"SELECT * FROM AgentNote WHERE CreatedByRepresentativeID = {repid}";
    # Runs and commits the data insertion
    cursor.execute(sql)
    tabledata = cursor.fetchall()
    return jsonify(tabledata)

# POST API for adding an agent's note
@application.route('/api/agentnote', methods=['POST'])
def create_agentnote():
    data = request.get_json()
    cursor = conn.cursor()

    sql = """
        INSERT INTO AgentNote (
            CreatedByRepresentativeID,
            NoteContent
        )
        VALUES (%s, %s)
    """

    values = (
        data['CreatedByRepresentativeID'],
        data['NoteContent']
    )

    cursor.execute(sql, values)
    conn.commit()

    return jsonify({'message': 'Agent note created successfully'}), 201

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
def put_data_no_id(table):
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
    conn.commit();
    return "DELETE Request Sucessful"

# POST API for adding a table entry
@application.route('/api/<table>', methods=['POST'])
def add_data(table):
    request_data = request.get_json()

    # Extract keys and values from JSON
    keys = list(request_data.keys())
    values = list(request_data.values())

    # Create placeholders for parameterized query
    placeholders = ', '.join(['%s'] * len(values))
    columns = ', '.join(keys)

    # Build SQL using parameterized placeholders
    sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'

    try:
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({'message': 'Post Request Successful'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500


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
            p.Premium,
            p.PolicyStatus,
            p.CancelReason,
            p.CancelDate,
            p.CategoryID,
            p.SubcategoryID,
            p.CompanyID,
            p.Issuer,
            p.AgentRecordID,
            p.RepresentativeID,
            c.CategoryName,
            s.SubcategoryName,
            co.CompanyName,
            CONCAT(r.FirstName, ' ', r.LastName) AS RepresentativeName,
            CONCAT(a_r.FirstName, ' ', a_r.LastName) AS AgentName
        FROM Policy p
        LEFT JOIN Category c ON p.CategoryID = c.CategoryID
        LEFT JOIN Subcategory s ON p.SubcategoryID = s.SubcategoryID
        LEFT JOIN Company co ON p.CompanyID = co.CompanyID
        LEFT JOIN Representative r ON p.RepresentativeID = r.RepresentativeID
        LEFT JOIN AgentOfRecord a ON p.AgentRecordID = a.AgentRecordID
        LEFT JOIN Representative a_r ON a.RepresentativeID = a_r.RepresentativeID
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


# Get household members by customer
@application.route('/api/customer/<int:customer_id>/householdmember', methods=['GET'])
def get_household_members(customer_id):
    sql = "SELECT * FROM HouseholdMember WHERE CustomerID = %s AND IsActive = 1"
    cursor.execute(sql, (customer_id,))
    members = cursor.fetchall()
    return jsonify(members)


# Add new household member
@application.route('/api/customer/<int:customer_id>/householdmember', methods=['POST'])
def add_household_member(customer_id):
    data = request.get_json()
    sql = """
        INSERT INTO HouseholdMember (
            CustomerID, FirstName, LastName, DateOfBirth,
            Gender, MaritalStatus, SSN, Relationship
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        customer_id,
        data['FirstName'],
        data['LastName'],
        data['DateOfBirth'],
        data['Gender'],
        data['MaritalStatus'],
        data['SSN'],
        data['Relationship']
    )
    cursor.execute(sql, values)
    conn.commit()
    return jsonify({'message': 'Household member added'}), 201


# Update household member
@application.route('/api/householdmember/<int:member_id>', methods=['PUT'])
def update_household_member(member_id):
    data = request.get_json()
    sql = """
        UPDATE HouseholdMember SET
            FirstName = %s,
            LastName = %s,
            DateOfBirth = %s,
            Gender = %s,
            MaritalStatus = %s,
            SSN = %s,
            Relationship = %s,
            IsActive = %s
        WHERE HouseholdMemberID = %s
    """
    values = (
        data['FirstName'],
        data['LastName'],
        data['DateOfBirth'],
        data['Gender'],
        data['MaritalStatus'],
        data['SSN'],
        data['Relationship'],
        data.get('IsActive', 1),
        member_id
    )
    cursor.execute(sql, values)
    conn.commit()
    return jsonify({'message': 'Household member updated'})


# Soft delete
@application.route('/api/householdmember/<int:member_id>', methods=['DELETE'])
def delete_household_member(member_id):
    sql = "UPDATE HouseholdMember SET IsActive = 0 WHERE HouseholdMemberID = %s"
    cursor.execute(sql, (member_id,))
    conn.commit()
    return jsonify({'message': 'Household member deactivated'})


# Get all relationships for a customer
@application.route('/api/customer/<int:customer_id>/relationships', methods=['GET'])
def get_customer_relationships(customer_id):
    sql = """
        SELECT 
            cr.CustomerRelationshipID,
            cr.ReferredCustomerID,
            c.FirstName,
            c.LastName,
            cr.CustomerRelation
        FROM CustomerRelationship cr
        JOIN Customer c ON c.CustomerID = cr.ReferredCustomerID
        WHERE cr.ReferrerCustomerID = %s
    """
    cursor.execute(sql, (customer_id,))
    relationships = cursor.fetchall()
    return jsonify(relationships)


# Add new relationship (and reverse)
@application.route('/api/customer/<int:customer_id>/relationships', methods=['POST'])
def add_customer_relationship(customer_id):
    data = request.get_json()
    referred_id = data['ReferredCustomerID']
    relation = data.get('CustomerRelation', '')

    # Prevent duplicate
    check_sql = """
        SELECT * FROM CustomerRelationship 
        WHERE ReferrerCustomerID = %s AND ReferredCustomerID = %s
    """
    cursor.execute(check_sql, (customer_id, referred_id))
    if cursor.fetchone():
        return jsonify({'message': 'Relationship already exists'}), 409

    # Insert main
    insert_sql = """
        INSERT INTO CustomerRelationship (
            ReferrerCustomerID, ReferredCustomerID, CustomerRelation
        ) VALUES (%s, %s, %s)
    """
    cursor.execute(insert_sql, (customer_id, referred_id, relation))

    # Insert reverse
    reverse_relation = data.get('CustomerRelationReverse', relation)
    cursor.execute(insert_sql, (referred_id, customer_id, reverse_relation))

    conn.commit()
    return jsonify({'message': 'Relationship added'}), 201


# Delete relationship (both sides)
@application.route('/api/customer-relationships/<int:relationship_id>', methods=['DELETE'])
def delete_customer_relationship(relationship_id):
    # Get IDs before deleting
    cursor.execute("SELECT ReferrerCustomerID, ReferredCustomerID FROM CustomerRelationship WHERE CustomerRelationshipID = %s", (relationship_id,))
    rel = cursor.fetchone()
    if not rel:
        return jsonify({'error': 'Relationship not found'}), 404

    cursor.execute("""
        DELETE FROM CustomerRelationship 
        WHERE (ReferrerCustomerID = %s AND ReferredCustomerID = %s)
           OR (ReferrerCustomerID = %s AND ReferredCustomerID = %s)
    """, (rel['ReferrerCustomerID'], rel['ReferredCustomerID'], rel['ReferredCustomerID'], rel['ReferrerCustomerID']))
    conn.commit()
    return jsonify({'message': 'Relationship deleted'})


# API for adding a new policy
@application.route('/api/policy', methods=['POST'])
def add_policy():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Create SQL query for inserting a new policy
        sql = """
        INSERT INTO Policy (
            CompanyID, AgentRecordID, CategoryID, SubcategoryID, 
            RepresentativeID, PolicyNumber, Issuer, 
            EffectiveDate, ExpirationDate, AdditionalInfo, Premium, CustomerID
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        # Prepare values for insertion
        values = (
            data.get('CompanyID'), 
            data.get('AgentRecordID'),
            data.get('CategoryID'),
            data.get('SubcategoryID'),
            data.get('RepresentativeID'),
            data.get('PolicyNumber'),
            data.get('Issuer'),
            data.get('EffectiveDate'),
            data.get('ExpirationDate'),
            data.get('AdditionalInfo'),
            data.get('Premium'),
            data.get('CustomerID')
        )
        
        # Execute the SQL query
        cursor.execute(sql, values)
        
        # Get the ID of the last inserted row
        policy_id = cursor.lastrowid
        
        # Commit the changes
        conn.commit()
        
        # Return the newly created policy ID
        return jsonify({
            'message': 'Policy added successfully',
            'PolicyID': policy_id
        }), 201
        
    except Exception as e:
        # Log the error
        print(f"Error adding policy: {str(e)}")
        
        # Roll back any changes if an error occurs
        conn.rollback()
        
        # Return error response
        return jsonify({
            'error': 'Failed to add policy',
            'details': str(e)
        }), 500

# API for getting categories
@application.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        # Create a new cursor for each request to avoid potential issues
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        sql = "SELECT CategoryID, CategoryName FROM Category"
        cursor.execute(sql)
        
        # Fetch all results explicitly
        categories = cursor.fetchall()
        
        # Convert any non-serializable values to strings
        result = []
        for category in categories:
            serializable_category = {}
            for key, value in category.items():
                # Handle type conversion for non-serializable types
                if isinstance(value, (datetime, date, timedelta, bytes, bytearray)):
                    serializable_category[key] = str(value)
                else:
                    serializable_category[key] = value
            result.append(serializable_category)
        
        return jsonify(result)
    except Exception as e:
        # Log detailed error information
        print(f"Error fetching categories: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return a helpful error message
        return jsonify({
            'error': 'Failed to fetch categories',
            'details': str(e)
        }), 500

# API for getting subcategories by category
@application.route('/api/categories/<int:category_id>/subcategories', methods=['GET'])
def get_subcategories(category_id):
    try:
        # Make sure to convert category_id to an integer
        category_id = int(category_id)
        
        # Use parameterized query to prevent SQL injection
        sql = "SELECT SubcategoryID, SubcategoryName FROM Subcategory WHERE CategoryID = %s"
        cursor.execute(sql, (category_id,))
        
        # Fetch all results
        subcategories = cursor.fetchall()
        
        # Return empty list if none found
        if not subcategories:
            return jsonify([])
            
        return jsonify(subcategories)
    except Exception as e:
        print(f"Error fetching subcategories: {str(e)}")
        # Return a useful error message and empty list
        return jsonify([]), 500


# API for getting companies
@application.route('/api/companies', methods=['GET'])
def get_companies():
    try:
        sql = "SELECT CompanyID, CompanyName FROM Company"
        cursor.execute(sql)
        companies = cursor.fetchall()
        return jsonify(companies)
    except Exception as e:
        print(f"Error fetching companies: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch companies',
            'details': str(e)
        }), 500

# API for getting agents of record
@application.route('/api/agents', methods=['GET'])
def get_agents():
    try:
        sql = """

            SELECT 
                a.AgentRecordID,
                r.RepresentativeID,
                CONCAT_WS(' ', r.FirstName, r.MiddleName, r.LastName, r.Suffix) AS FullName,
                a.StartDate,
                a.EndDate,
                a.Status,
                a.Notes
            FROM AgentOfRecord a
            JOIN Representative r ON a.RepresentativeID = r.RepresentativeID;
        """
        cursor.execute(sql)
        agents = cursor.fetchall()
        return jsonify(agents)
    except Exception as e:
        print(f"Error fetching agents: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch agents',
            'details': str(e)
        }), 500

# Policy management endpoints
@application.route('/api/policy/<int:policy_id>', methods=['POST'])
def update_policy(policy_id):
    """Update an existing policy"""
    try:
        data = request.get_json()
        
        # Create SQL query for updating a policy
        sql = """
        UPDATE Policy SET
            CompanyID = %s,
            CategoryID = %s,
            SubcategoryID = %s,
            PolicyNumber = %s,
            Issuer = %s,
            EffectiveDate = %s,
            ExpirationDate = %s,
            Premium = %s,
            AgentRecordID = %s,
            RepresentativeID = %s,
            AdditionalInfo = %s
        WHERE PolicyID = %s
        """
        
        values = (
            data.get('CompanyID'),
            data.get('CategoryID'),
            data.get('SubcategoryID'),
            data.get('PolicyNumber'),
            data.get('Issuer'),
            data.get('EffectiveDate'),
            data.get('ExpirationDate'),
            data.get('Premium'),
            data.get('AgentRecordID'),
            data.get('RepresentativeID'),
            data.get('AdditionalInfo'),
            policy_id
        )
        
        cursor.execute(sql, values)
        conn.commit()
        
        return jsonify({
            'message': 'Policy updated successfully',
            'PolicyID': policy_id
        })
        
    except Exception as e:
        print(f"Error updating policy: {str(e)}")
        conn.rollback()
        return jsonify({
            'error': 'Failed to update policy',
            'details': str(e)
        }), 500

@application.route('/api/policy/<int:policy_id>/rewrite', methods=['POST'])
def rewrite_policy(policy_id):
    """Rewrite a policy (create a new one based on the old one but with different terms)"""
    try:
        data = request.get_json()
        
        # First, mark the original policy as rewritten
        update_sql = """
        UPDATE Policy SET
            PolicyStatus = 'Rewritten'
        WHERE PolicyID = %s
        """
        cursor.execute(update_sql, (policy_id,))
        
        # Then, create a new policy with the updated data
        insert_sql = """
        INSERT INTO Policy (
            CustomerID, CompanyID, CategoryID, SubcategoryID, 
            PolicyNumber, Issuer, EffectiveDate, ExpirationDate,
            Premium, AgentRecordID, RepresentativeID, AdditionalInfo,
            PolicyStatus
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active'
        )
        """
        
        values = (
            data.get('CustomerID'),
            data.get('CompanyID'),
            data.get('CategoryID'),
            data.get('SubcategoryID'),
            data.get('PolicyNumber'),
            data.get('Issuer'),
            data.get('EffectiveDate'),
            data.get('ExpirationDate'),
            data.get('Premium'),
            data.get('AgentRecordID'),
            data.get('RepresentativeID'),
            data.get('AdditionalInfo')
        )
        
        cursor.execute(insert_sql, values)
        new_policy_id = cursor.lastrowid
        
        conn.commit()
        
        return jsonify({
            'message': 'Policy rewritten successfully',
            'OriginalPolicyID': policy_id,
            'PolicyID': new_policy_id
        })
        
    except Exception as e:
        print(f"Error rewriting policy: {str(e)}")
        conn.rollback()
        return jsonify({
            'error': 'Failed to rewrite policy',
            'details': str(e)
        }), 500

@application.route('/api/policy/<int:policy_id>/renew', methods=['POST'])
def renew_policy(policy_id):
    """Renew a policy (create a new one with a new date range)"""
    try:
        data = request.get_json()
        
        # First, mark the original policy as renewed
        update_sql = """
        UPDATE Policy SET
            PolicyStatus = 'Renewed'
        WHERE PolicyID = %s
        """
        cursor.execute(update_sql, (policy_id,))
        
        # Then, create a new policy with the renewed data
        insert_sql = """
        INSERT INTO Policy (
            CustomerID, CompanyID, CategoryID, SubcategoryID, 
            PolicyNumber, Issuer, EffectiveDate, ExpirationDate,
            Premium, AgentRecordID, RepresentativeID, AdditionalInfo,
            PolicyStatus
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active'
        )
        """
        
        values = (
            data.get('CustomerID'),
            data.get('CompanyID'),
            data.get('CategoryID'),
            data.get('SubcategoryID'),
            data.get('PolicyNumber'),
            data.get('Issuer'),
            data.get('EffectiveDate'),
            data.get('ExpirationDate'),
            data.get('Premium'),
            data.get('AgentRecordID'),
            data.get('RepresentativeID'),
            data.get('AdditionalInfo')
        )
        
        cursor.execute(insert_sql, values)
        new_policy_id = cursor.lastrowid
        
        conn.commit()
        
        return jsonify({
            'message': 'Policy renewed successfully',
            'OriginalPolicyID': policy_id,
            'PolicyID': new_policy_id
        })
        
    except Exception as e:
        print(f"Error renewing policy: {str(e)}")
        conn.rollback()
        return jsonify({
            'error': 'Failed to renew policy',
            'details': str(e)
        }), 500

@application.route('/api/policy/<int:policy_id>/cancel', methods=['POST'])
def cancel_policy(policy_id):
    """Cancel a policy"""
    try:
        data = request.get_json()
        
        # Mark the policy as canceled
        update_sql = """
        UPDATE Policy SET
            PolicyStatus = 'Canceled',
            CancelReason = %s,
            CancelDate = %s
        WHERE PolicyID = %s
        """
        
        values = (
            data.get('CancelReason'),
            data.get('CancelDate') or datetime.now().strftime('%Y-%m-%d'),
            policy_id
        )
        
        cursor.execute(update_sql, values)
        conn.commit()
        
        return jsonify({
            'message': 'Policy canceled successfully',
            'PolicyID': policy_id
        })
        
    except Exception as e:
        print(f"Error canceling policy: {str(e)}")
        conn.rollback()
        return jsonify({
            'error': 'Failed to cancel policy',
            'details': str(e)
        }), 500
    

# Get all notes for a specific customer
@application.route('/api/customer/<int:customer_id>/notes', methods=['GET'])
@cross_origin()
def get_customer_notes(customer_id):
    sql = """
        SELECT 
            n.NoteID,
            n.CustomerID,
            n.CreatedByRepresentativeID,
            n.PolicyID,
            n.CustomerName,
            n.PolicyName,
            n.DateCreated,
            n.NoteType,
            n.NoteContent,
            CONCAT(r.FirstName, ' ', r.LastName) AS RepresentativeName
        FROM Note n
        LEFT JOIN Representative r ON n.CreatedByRepresentativeID = r.RepresentativeID
        WHERE n.CustomerID = %s
        ORDER BY n.DateCreated DESC
    """
    
    cursor.execute(sql, (customer_id,))
    notes = cursor.fetchall()
    

    # Handle datetime serialization
    def convert(val):
        if isinstance(val, (datetime, date, timedelta)):
            return str(val)
        return val

    # Convert all values to be JSON serializable
    result = [
        {key: convert(value) for key, value in note.items()}
        for note in notes
    ]
    
    return jsonify(result)

# Create a new note
@application.route('/api/note', methods=['POST'])
def create_note():
    data = request.get_json()
    
    sql = """
        INSERT INTO Note (
            CustomerID,
            CreatedByRepresentativeID,
            PolicyID,
            CustomerName,
            PolicyName,
            NoteType,
            NoteContent
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        data.get('CustomerID'),
        data.get('CreatedByRepresentativeID'),
        data.get('PolicyID'),
        data.get('CustomerName'),
        data.get('PolicyName'),
        data.get('NoteType'),
        data.get('NoteContent')
    )
    
    cursor.execute(sql, values)
    note_id = cursor.lastrowid
    conn.commit()
    
    return jsonify({
        'message': 'Note created successfully',
        'NoteID': note_id
    }), 201

# Delete a note
@application.route('/api/note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    sql = "DELETE FROM Note WHERE NoteID = %s"
    cursor.execute(sql, (note_id,))
    conn.commit()
    
    return jsonify({
        'message': 'Note deleted successfully'
    })

if __name__ == "__main__":
    application.run(debug=True, threaded=True)