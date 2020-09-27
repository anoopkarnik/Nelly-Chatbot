# nelly_services 
The service layer for Nelly 

Steps to execute for a successful run (Ubuntu)

To create the virtual environment in nelly_auth folder, run the below command

python3 -m venv venv

To start using this virtual environment, you need to activate it by running the activate script

source venv/bin/activate

Install Flask and other dependencies

pip install Flask

pip install requests 

pip install python-jose

pip install Flask-restful

pip install Flask-MySQLdb

Test the development environment 

export FLASK_APP=nelly_service

flask run


pip3 install -r requirements.txt 