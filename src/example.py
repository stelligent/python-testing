'''
Example file with boto3 calls that we will write tests for
'''
import os
import sys
from typing import Optional
import logging
import boto3
import botocore.exceptions

logging.basicConfig(
    level=logging.DEBUG if os.environ.get('DEBUG') else logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

def get_certificate(thing: str, client: Optional[boto3.client] = None) -> str:
    '''
    Get a certificate AWS IoT certificate ID

    Parameters:
        thing (str): The IoT Thing Name
        client (boto3.client): A boto3 IoT client

    Returns: str
    '''
    iot_client = client or boto3.client('iot')

    principals = []
    try:
        response = iot_client.list_thing_principals(
            thingName=thing,
        )
        principals = response['principals']
    except botocore.exceptions.ClientError as err:
        logging.warning('Error calling iot_client.list_thing_principals %s', err)
        if err.response['Error']['Code'] != 'ResourceNotFoundException':
            raise err

    certs = list(filter(lambda principal: ':cert/' in principal, principals))
    if certs:
        return certs

    certs = iot_client.create_keys_and_certificate(
        setAsActive=True,
    )

    return [certs['certificateArn']]

class MyS3Class:
    '''
    MyS3Class controls interactions with S3 through the boto3 client
    '''
    #
    # boto3 S3 client
    #
    s3_client: boto3.client
    #
    # bucket used on S3 operations
    #
    bucket: str

    def __init__(self, bucket: str, client: Optional[boto3.client] = None):
        self.s3_client = client or boto3.client('s3')
        self.bucket = bucket

    def upload_file(self, data: bytearray, key: str) -> None:
        '''
        Upload a file to S3
        '''
        return self.s3_client.upload_fileobj(data, self.bucket, key)

    def get_file(self, bucket: str, key: str, client: Optional[boto3.client] = None) -> dict:
        '''
        Get a file from S3
        '''
        raise Exception('no implimented')
