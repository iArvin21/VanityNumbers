# Vanity Numbers Generator
This repo contains :
1. A lambda function that generates a list of vanity numbers using the customer's phone number as the input then saves them into a DynamoDB.
2. Instructions for Amazon Connect setup
3. A simple web app that displays the vanity numbers

## Usage

### AWS Services
1. AWS Lambda
2. DynamoDB
3. Amazon Connect

### Lambda Configuration
Create a lambda function that generates and saves vanity numbers to DynamoDB
1. Create a Lambda function with runtime Python 3.10 and use the provided lambda_function.py
2. To use nltk library, upload py_nltk.zip to lambda layers then add the created layer to your lambda function
3. Create a DynamoDB for your lambda function
4. To access DynamoDB add the policies to the automatically created IAM role for your lambda function
5. Create a test event for your lambda function using the test_event.json file, this is a sample json format for Amazon Connect integration

### Amazon Connect
Setup an Amazon connect flow with lambda integration
1. Create an Amazon Connect instance
2. Open your instance Flows configuration, navigate to AWS Lambda and add the lambda function that you created
3. Open Amazon Connect instance and create a new flow, add an invoke AWS Lambda function and set the destination key as 'phone_number'
![image](https://github.com/iArvin21/VanityNumbers/assets/48306733/0b1d784d-820b-4019-a848-7006d41e7def)
4. Create a play prompt that will output the results of your lambda function
![image](https://github.com/iArvin21/VanityNumbers/assets/48306733/0d0fa66d-0480-4187-90ca-fc044e75657d)

### Web App
This repository also includes a simple web app (vanity_numbers folder) that displays the generated vanity numbers for the last 5 callers.
1. First create a directory for your webapp
```
mkdir vanity_numbers
cd vanity_numbers
```
2. Create a python virtual environment
```
python -m venv venv
```
3. Activate the virtual environment
```
venv\Scripts\activate
```
4. Install flask and boto3
```
pip install flask boto3
```
5. Add the contents of web_app folder on your project directory then run your flask application
```
python app.py
```
6. You can check the web app on your local environment using http://localhost:5000
![image](https://github.com/iArvin21/VanityNumbers/assets/48306733/64693013-dbb7-463f-98ad-89e098db2056)

