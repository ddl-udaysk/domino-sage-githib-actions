from chalice import Chalice
import os
import io
import boto3
import json
import csv


app = Chalice(app_name='api-endpoint')
runtime= boto3.client('runtime.sagemaker')

model_name = os.environ['MODELNAME']
ENDPOINT_NAME = model_name+ "endpoint"

@app.route('/')
def index():
    return {'hello': 'world'}



@app.route('/api', methods=['POST'] , content_types=['application/json'])
def create_user():
#     # This is the JSON body the user sent in their POST request.
    userdata_as_json = app.current_request.json_body
    payload=json.dumps(userdata_as_json)
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                               ContentType='application/json',
                                               Body=payload)
    result = json.loads(response['Body'].read().decode())
#     # We'll echo the json body back to the user in a 'user' key.
    return  result
#
# See the README documentation for more examples.
#
