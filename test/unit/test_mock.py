'''
Test our example file using magic mock.
Monkeypatches the boto3 request object.
'''
from unittest import mock
import pytest
from botocore.exceptions import ClientError
from src.example import get_certificate

class MockResponse:
    '''
    Class to Mock urllib3 response
    '''
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def __iter__(self) -> any:
        '''
        Need to implement iterable in order to be representable
        '''
        for value in [self, self.body]:
            yield value

    def __repr__(self) -> (any, str):
        '''
        Overload the representation of the object for
        assigning values from this class when destructuring
        '''
        return repr([self, self.body])

def boto_client_error(code: str, method: str, message: str = r'¯\_(ツ)_/¯'):
    '''
    Create a boto3 ClientError
    '''
    return ClientError(
        {
            'Error': {
                'Code': code,
                'Message': message,
            },
        },
        method,
    )

@mock.patch('botocore.client.BaseClient._make_request')
def test_get_thing_and_certificate_exists(mock_api):
    '''
    Test getting a thing with an existing certificate
    '''
    mock_api.return_value = MockResponse(
        200,
        {
            'principals': [
                'arn:aws:iot:region:account_id:cert/foobar',
                'arn:aws:iot:region:account_id:cert/baz',
            ],
        },
    )
    cert = get_certificate(thing='my-test-core')
    assert cert == [
        'arn:aws:iot:region:account_id:cert/foobar',
        'arn:aws:iot:region:account_id:cert/baz',
    ]

@mock.patch('botocore.client.BaseClient._make_request')
def test_get_thing_exists_certificate_creates(mock_api):
    '''
    Assert that a new certificate is generated if the thing exists
    but no certificates are attached
    '''
    mock_api.side_effect = [
        MockResponse(
            200,
            {
                'principals': [],
            }
        ),
        MockResponse(
            200,
            {
                'certificateArn': 'arn:aws:iot:region:account_id:cert/foobar',
                'certificateId': 'barbaz',
                'certificatePem': 'foo',
                'keyPair': {
                    'PublicKey': 'bar',
                    'PrivateKey': 'baz',
                },
            },
        ),
    ]
    cert = get_certificate(thing='my-test-core')
    assert cert == ['arn:aws:iot:region:account_id:cert/foobar']

@mock.patch('botocore.client.BaseClient._make_request')
def test_get_certificate_no_thing_cert_creates(mock_api):
    '''
    Test that a certificate is created if no thing exists and returns the cert
    '''
    mock_api.side_effect = [
        boto_client_error(
            'ResourceNotFoundException',
            'list_thing_principals'
        ),
        MockResponse(
            200,
            {
                'certificateArn': 'arn:aws:iot:region:account_id:cert/foobar',
                'certificateId': 'barbaz',
                'certificatePem': 'foo',
                'keyPair': {
                    'PublicKey': 'bar',
                    'PrivateKey': 'baz',
                },
            },
        ),
    ]
    cert = get_certificate(thing='my-test-core')
    assert cert == ['arn:aws:iot:region:account_id:cert/foobar']

@mock.patch('botocore.client.BaseClient._make_request')
def test_get_certificate_thing_exception(mock_api):
    '''
    Assert that an exception is thrown if the request fails and
    is not a ResourceNotFoundExeption
    '''
    mock_api.side_effect = ClientError(
        {
            'Error':{
                'Code': 'InvalidRequestException',
                'Message': 'something went wrong',
            }
        },
        'list_thing_principals'
    )
    with pytest.raises(ClientError):
        get_certificate(thing='my-test-core')
