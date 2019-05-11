'''
Test our example file using boto3 Stubber.
Methods must support dependency injection
in order to stub tests.
'''
from unittest import mock
import pytest
import botocore.session
from botocore.stub import Stubber, ANY
from src.example import get_certificate

def test_get_thing_and_certificate_exists():
    '''
    Test getting a thing with an existing certificate
    '''
    client = botocore.session.get_session().create_client('iot')
    stubber = Stubber(client)
    response = {
        'principals': [
            'arn:aws:iot:region:account_id:cert/foobar',
            'arn:aws:iot:region:account_id:cert/baz',
        ],
    }
    expected_params = {'thingName': 'my-test-core'}
    stubber.add_response('list_thing_principals', response, expected_params)
    stubber.activate()

    cert = get_certificate(
        thing='my-test-core',
        client=client,
    )
    assert cert == [
        'arn:aws:iot:region:account_id:cert/foobar',
        'arn:aws:iot:region:account_id:cert/baz',
    ]

def test_get_thing_exists_certificate_creates():
    '''
    Assert that a new certificate is generated if the thing exists
    but no certificates are attached
    '''
    client = botocore.session.get_session().create_client('iot')
    stubber = Stubber(client)
    response_list = {
        'principals': [],
    }
    response_create = {
        'certificateArn': 'arn:aws:iot:region:account_id:cert/0000000000000000000000000000000000000000000000000000000000000000',
        'certificateId': '0000000000000000000000000000000000000000000000000000000000000000',
        'certificatePem': 'foo',
        'keyPair': {
            'PublicKey': 'bar',
            'PrivateKey': 'baz',
        },
    }
    stubber.add_response('list_thing_principals', response_list, {'thingName': ANY})
    stubber.add_response('create_keys_and_certificate', response_create, {'setAsActive': ANY})
    stubber.activate()

    cert = get_certificate(
        thing='my-test-core',
        client=client,
    )
    assert cert == ['arn:aws:iot:region:account_id:cert/0000000000000000000000000000000000000000000000000000000000000000']

def test_get_thing_exists_certificate_creates_monkeypatch():
    '''
    Assert that a new certificate is generated if the thing exists
    but no certificates are attached
    '''
    client = botocore.session.get_session().create_client('iot')
    stubber = Stubber(client)
    response = {
        'principals': [
            'arn:aws:iot:region:account_id:cert/foobar',
            'arn:aws:iot:region:account_id:cert/baz',
        ],
    }
    expected_params = {'thingName': 'my-test-core'}
    stubber.add_response('list_thing_principals', response, expected_params)
    stubber.activate()

    # We're going to patch the boto3 import in src.example
    with mock.patch('src.example.boto3') as mock_boto3:
        # Tell our mock object to return our own client when boto3.client is called
        mock_boto3.client.return_value = client
        cert = get_certificate(
            thing='my-test-core',
        )
        assert cert == [
            'arn:aws:iot:region:account_id:cert/foobar',
            'arn:aws:iot:region:account_id:cert/baz',
        ]
