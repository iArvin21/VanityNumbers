import boto3
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Enable auto-reloading
app.debug = True

# Replace the values with your AWS access key and secret key
ACCESS_KEY = ''
SECRET_KEY = ''

# Replace the values with your DynamoDB table name and region
TABLE_NAME = ''
REGION_NAME = ''

@app.route('/')
def index():
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)
    
    # Get all items from the table
    response = table.scan()
    items = response['Items']

    # sort items by added_date attribute (in descending order)
    items = sorted(items, key=lambda x: datetime.strptime(x['added_date'], '%d/%m/%Y %H:%M:%S'), reverse=True)
    
    # get the latest 5 items
    latest_items = items[:5]
    

    return render_template('index.html', items=latest_items)

if __name__ == '__main__':
    app.run(debug=True)
