# python_spacex_proxy


To run localy, enter the `spacex_proxy` directory, then enter the following command in a terminal: `chalice local`

Then, visit one of the following links to see the routes that have been defined:

http://127.0.0.1:8000/
The root will display json that aggregates the two spacex urls

http://127.0.0.1:8000/launches
This shows the launches prior to aggregation (mostly used for debugging)

http://127.0.0.1:8000/rockets
This shows the pruned list of rockets


I have staged this script in an AWS Lambda function using Chalice. It can be accessed via `https://nkrienmngh.execute-api.us-east-2.amazonaws.com/api/`.
