'''
Test our example file using magic mock
'''
from unittest import mock
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


@mock.patch('botocore.client.BaseClient._make_request')
def test_get_certificate_exists(mock_api):
    '''
    Test getting a thing with an existing certificate
    '''
    response = MockResponse(200, {
        'principals': [
            'abc123',
        ],
    })

    mock_api.return_value = response

    cert = get_certificate('my-test-core')
    assert cert == 'abc123'
