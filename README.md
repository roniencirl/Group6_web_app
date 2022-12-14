# Group6_web_app

## Placeholder for MSCCYB1, Secure Programming for Web Group 6 project code.

The 'clabaireacht' web app allows users to post messages and images in an informal journal style form for visitors or other users to read. 
In Gaelige 'clabaireacht' means chit-chat or babbling. Pronunciation: https://www.teanglann.ie/en/fuaim/clabaireacht

## Requirements

pipenv - to ensure python versioning and dependencies.
https://pipenv.pypa.io/en/latest/
https://pipenv-fork.readthedocs.io/en/latest/basics.html

$ pipenv install
$ pipenv shell


## Working in this repo:

Due to the small number of teams members, we will keep our branching strategy simple. 

The main branch can be checked out to a locally named branch.  

Pull requests can be raised directly against the main branch on github. 

Commits must include a brief description of the changes made.  

PRs must include a description what has changed, what may be missing, and any testing carried out. 

PRs must be approved by one other team member before being merged (github enforced)

PRs should must be merged with the remote branch HEAD before being raised.  

Work will be divided to avoid too many team members working on the same area of code at once. 

If you are working on code you should commit your changes when done. 

Makefiles are configured for linting, formating, SAST and dependency checks. 
Note a Docker Hub login is required for some checks.

to perform all python checks run:
$ make python_check

to format with black run:
$ make python_check_format


TODO:
* add a Makefile for format, check and test. [Done]

Running locally:
Quick: 
make run_dev 

Details:
./Group6_web_app $ pipenv update 
./Group6_web_app $ pipenv shell
(Group6_web_app-aBsMno69) ronie@debian:~/Masters/SPW/Group6_web_app_main$ cd src/
(Group6_web_app-aBsMno69) ronie@debian:~/Masters/SPW/Group6_web_app_main/src$ flask --app clabaireacht --debug run
clabaireacht
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
clabaireacht
<Config {'ENV': 'production', 'DEBUG': True, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'SECRET_KEY': 'dev', 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(seconds=1800), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': 'Lax', 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': None, 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'JSON_AS_ASCII': None, 'JSON_SORT_KEYS': None, 'JSONIFY_PRETTYPRINT_REGULAR': None, 'JSONIFY_MIMETYPE': None, 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093, 'DATABASE': '/home/ronie/Masters/SPW/Group6_web_app/src/instance/clabaireacht.sqlite', 'PW_PEPPER_SECRET': '', 'MAX_CONTEXT_LENGTH': 16777216, 'LOCK_ACCOUNT_DAYS': 30}>
 * Debugger is active!
 * Debugger PIN: 


# WIP - this section is a work in progress
## Quickstart running in production.
Quick: make run_prod


## Running in production:
### Install gunicorn
from https://gunicorn.org/
$ python3 -m pip install gunicorn

### While testing you can use a self signed certificate.
./Group65_web_app $ mkdir ssl 
./Group6_web_app $ openssl req -x509 -newkey rsa:4096 -keyout ./ssl/key.pem -out ./ssl/cert.pem -sha256 -days 30 -nodes -subj '/CN=localhost'

###
gunicorn -w 1 'clabaireacht:create_app()' --keyfile ../ssl/key.pem --certfile ../ssl/cert.crt 

