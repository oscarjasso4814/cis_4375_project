# cis_4375_project

group 1 repository

## Frontend
Vue.js 3 App

Running front-end:

*File named "apiurl.js" needs to be added in crm-app/api directory from Teams

```
cd crm-app
npm install
npm run dev
```

For local deployment, create "apiurl.js" under crm-app/src/api with the following code:
```
export const url = "http://127.0.0.1:5000";
```

For Elastic Beanstalk deployment, zip the contents of the flask-backend folder (not the folder itself) and upload to application. Provide database credentials as credsHelp.py prior to zipping. Provide the same code as above but replace URL with Elastic Beanstalk domain.

## Backend
Python Flask

Running back-end:

*File named "credsHelp.py" needs to be added in flask-backend directory from Teams



```
cd flask-backend
pip install flask
pip install Werkzeug==2.2.2
pip install flask_cors
pip install mysql.connector
py application.py
```