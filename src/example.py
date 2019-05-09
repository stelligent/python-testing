'''
Example file with boto3 calls that we will write tests for
'''
import os
import sys
import logging
import boto3

logging.basicConfig(
    level=logging.DEBUG if os.environ.get('DEBUG') else logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

def get_certificate(thing: str) -> str:
    '''
    Get the certificate ID for a thing
    If the certificate is not attached, or the thing does not
    exist, then a new cert is created and returned so it
    can be attached later.

    Parameter:
        thing (str): The IoT Thing Name

    Returns: str
    '''
    iot_client = boto3.client('iot')
    principals = []
    try:
        response = iot_client.list_thing_principals(
            thingName=thing,
        )
        principals = response['principals']
    except Exception as err: # pylint: disable=broad-except
        logging.warning('Error calling iot_client.list_thing_principals %s', err)

    return principals[0]
