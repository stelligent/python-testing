'''
Test our example file using moto.
Monkeypatches the boto3 request object.
'''
import boto3
from moto import mock_iot
from src.example import get_certificate

@mock_iot
def test_get_thing_and_certificate_exists():
    '''
    Test getting a thing with an existing certificate
    '''
    cert = get_certificate(thing='my-test-core')
    assert cert

    iot_client = boto3.client('iot')
    response = iot_client.list_thing_principals(
        thingName='my-test-core',
    )
    # Expected to fail because of missing iot implementation
    assert response['principals']
