import json
import boto3
import os
import random

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    randInt = random.randint(1, 39)
    
    response = table.get_item(
        Key={
            "id": randInt
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Headers' : '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(response["Item"]['quote'])
    }

