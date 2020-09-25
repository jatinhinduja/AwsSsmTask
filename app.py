from os import environ
import os
import json
import boto3
import os
from datetime import datetime
import time
import botocore

ENV = os.environ.get('ENV')
print("This is current" + str(ENV))
# stack_name='Stack101'
stack_name = os.environ.get('Stack_Name')
print("The stack is " + stack_name)
choice = os.environ.get('Choice')
if ENV == 'Dev':
    # Stack101
    cf_client = boto3.client('cloudformation', aws_access_key_id='',
                             aws_secret_access_key='', region_name='ap-south-1')
    TemplateUrl = 'http://s3bucketlink/VPC.yaml'


else:
    print("Please choose Dev or Prod")
    exit()


def fetch_s3():
    s3 = boto3.resource('s3')
    buckets = s3.buckets.all()
    for bucket in buckets:
        print(bucket.name)


def validate_template():

    response = cf_client.validate_template(

        TemplateURL=TemplateUrl
    )
    return response


def launch_stack():

    print(cf_client)
    print(TemplateUrl)
    stack_data = cf_client.create_stack(
        StackName=stack_name,
        TemplateURL=TemplateUrl,
        Parameters=[
            {
                'ParameterKey': 'AdministratorAccountId',
                'ParameterValue': '798',

            },
            {
                'ParameterKey': 'Environment',
                'ParameterValue': ENV,

            },

        ],
        Capabilities=[
            'CAPABILITY_NAMED_IAM'
        ],
        Tags=[
            {
                'Key': 'Environment',
                'Value': ENV
            }
        ]
    )

    return stack_data


def update_stack():

    stack_data = cf_client.update_stack(
        StackName=stack_name,
        TemplateURL=TemplateUrl,
        Parameters=[
            {
                'ParameterKey': 'AdministratorAccountId',
                'ParameterValue': '798',

            },
            {
                'ParameterKey': 'Environment',
                'ParameterValue': ENV,

            },

        ],
        Capabilities=[
            'CAPABILITY_NAMED_IAM'
        ],
        Tags=[
            {
                'Key': 'Environment',
                'Value': ENV
            }
        ]
    )

    return stack_data


def check_resources():

    response = cf_client.list_stack_resources(
        StackName=stack_name
    )
    return response


def stack_exists():

    stacks = cf_client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False


def launch_update():
    try:
        if stack_exists():
            print("--------UPDATING STACK------------")
            stack_result = update_stack()

            print(stack_result)

        else:
            print("---------CREATING STACK------------")
            stack_result = launch_stack()
            print(stack_result)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")



def delete_stack():

    if stack_exists():
        print("------------Deleting Stack-----------")
        stack_result = cf_client.delete_stack(StackName=stack_name)
        print(stack_result)

    else:
        print("Stack Not Found")


def launcher():

    print("-------------------------------------------------")

    ch='1'
    if ch == '1':
        launch_update()
        time.sleep(20)
        print("--------------------------------------------------")
        print(check_resources())
    elif ch == '2':
        delete_stack()
        time.sleep(20)
        print("--------------------------------------------------")
        print(check_resources())

    else:
        print("Please make correct choice")


launcher()