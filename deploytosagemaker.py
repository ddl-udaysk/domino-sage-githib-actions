import boto3
import os

client = boto3.client('sagemaker')

modelName = os.environ['MODELNAME']
instance_type = 'ml.t3.xlarge'

# create sagemaker model
create_model_api_response = client.create_model(
                                    ModelName='modelName',
                                    PrimaryContainer={
                                        'Image': '946429944765.dkr.ecr.us-west-2.amazonaws.com/bcs-sagemaker:'+ modelName,
                                        'ModelDataUrl': 's3://path/to/model/artifact/model.tar.gz',
                                        'Environment': {}
                                    },
                                    ExecutionRoleArn='ARN for AmazonSageMaker-ExecutionRole'
                            )

print ("create_model API response", create_model_api_response)

endpointconfiguration = modelName + "endpoint-configuration"
# create sagemaker endpoint config
create_endpoint_config_api_response = client.create_endpoint_config(
                                            EndpointConfigName=endpointconfiguration,
                                            ProductionVariants=[
                                                {
                                                    'VariantName': 'AllTraffic',
                                                    'ModelName': modelName,
                                                    'InitialInstanceCount': 1,
                                                    'InstanceType': instance_type
                                                },
                                            ]
                                       )

print ("create_endpoint_config API response", create_endpoint_config_api_response)

endpoint = modelName + "endpoint"
# create sagemaker endpoint
create_endpoint_api_response = client.create_endpoint(
                                    EndpointName=endpoint,
                                    EndpointConfigName=endpointconfiguration,
                                )

print ("create_endpoint API response", create_endpoint_api_response)            