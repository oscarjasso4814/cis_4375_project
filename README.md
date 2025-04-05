# cis_4375_project

group 1 repository

## Frontend
Vue.js 3 App

Running front-end:

```
cd crm-app
npm install
npm run dev
```

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

For Elastic Beanstalk, zip the flask-backend folder and upload to application. Provide database credentials as credsHelp.py prior to zipping.