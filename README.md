# python_spacex_proxy


To run localy, enter the following command in a terminal: `env FLASK_APP=flask-test.py flask run`

Then, visit one of the following links to see the routes that have been defined:

http://127.0.0.1:5000/
The root will display json that aggregates the two spacex urls

http://127.0.0.1:5000/launches
This shows the launches prior to aggregation (mostly used for debugging)

http://127.0.0.1:5000/rockets
This shows the pruned list of rockets


I intend on staging this script as an AWS Lambda function for my own education. Sometime.
