# Group6_web_app

## Placeholder for MSCCYB1, Secure Programming for Web Group 6 project code.

The 'clabaireact' web app allows users to post messages and images in an informal journal style form for visitors or other users to read. 
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

