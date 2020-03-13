# flasky-restApi-app
A complete restful api project that has been developing in flask. implements JWT authentication, role-based and content permission authorization and advanced mysql queries.

## Installation
install with git clone and change to new_project branch


	$ git clone https://github.com/Ali-Khakpash/flasky-restApi-app

 	$ git checkout new_project
  
 ## VirtualEnv
 this project uses virtualenv for handling dependencies.
 
 all you need to use virtualenv is using the following code in your project root directory
 ```
 source venv/bin/activate
 ```
 
  
  ## Configuration
  set configuration settings in config.py file
  
 for example, configure your database and email settings
 
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@127.0.0.1:3306/YOUR_DB_NAME'
MAIL_DEFAULT_SENDER = 'mail@example.com'
MAIL_SERVER = 'smtp.example.com'
MAIL_PORT = 587
MAIL_USERNAME = 'EMIAL USERNAME'
MAIL_PASSWORD = 'EMAIL PASSWORD'
```

## Run The Project

the following command will run the project on development environment

```
python3 run.py
```


