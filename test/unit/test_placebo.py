import boto3
import pytest
import placebo
from src.example import get_certificate

@pytest.fixture(scope='module')
def placebo_session():
    boto3.setup_default_session()
    session = boto3.DEFAULT_SESSION
    pill = placebo.attach(session, data_path='test/fixtures')
    pill.playback()

def test_get_thing_and_certificate_exists(placebo_session):
    '''
    Test getting a thing with an existing certificate
    '''
    cert = get_certificate(thing='my-test-core')
    print(cert)
    assert cert == [
        'arn:aws:iot:region:account_id:cert/0000000000000000000000000000000000000000000000000000000000000000',
    ]
