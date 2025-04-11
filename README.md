# cis_4375_project

group 1 repository

## Frontend
Vue.js 3 App


*File named "apiurl.js" needs to be added in crm-app/api directory (from Teams for group)

For Elastic Beanstalk deployment, zip the contents of the crm-app folder (not the folder itself) and upload to application. 
Provide api credentials as "apiurl.py" prior to zipping:

Create "apiurl.js" under crm-app/src/api with the following information:
```
export const url = "elasticbeanstalkurl";
```
For local flask backend deployment, use http://127.0.0.1:5000 as the URL

Running front-end locally:
```
cd crm-app
npm install
npm run dev
```


## Backend
Python Flask


*File named "credsHelp.py" needs to be added in flask-backend directory from Teams

For Elastic Beanstalk deployment, zip the contents of the flask-backend folder (not the folder itself) and upload to application. 
Provide database credentials as credsHelp.py prior to zipping. 
Create "credsHelp.py" in flask-backend with the following information: 
```
class Creds:
    conString = 'databaseendpointurl'
    userName = 'username'
    password = 'password'
    dbName = 'database1'
```

Running back-end locally:
```
cd flask-backend
pip install flask
pip install Werkzeug==2.2.2
pip install flask_cors
pip install mysql.connector
py application.py
```

