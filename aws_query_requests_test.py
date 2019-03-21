from aws_query_requests import Credentials, QueryRequest, QueryRequestHandler
import urllib
import json

def test_describe_regions(credentials, query_request_handler, region='us-east-1'):
    query_request = QueryRequest(
        credentials=credentials,
        method='GET',
        service="ec2",
        host='ec2.amazonaws.com',
        region='us-east-1',
        endpoint='https://ec2.amazonaws.com',
        content_type='application/x-www-form-urlencoded',
        request_parameters='Action=DescribeRegions&Version=2013-10-15'
    )
    query_request_handler.performRequest(query_request)

def test_describe_key_pairs(credentials, query_request_handler, region='us-east-1'):
    query_request = QueryRequest(
        credentials=credentials,
        method='GET',
        service="ec2",
        host='ec2.amazonaws.com',
        region='us-east-1',
        endpoint='https://ec2.amazonaws.com',
        content_type='application/x-www-form-urlencoded',
        request_parameters='Action=DescribeKeyPairs&Version=2013-10-15'
    )
    query_request_handler.performRequest(query_request)

def test_run_instances(credentials, query_request_handler, region='us-east-1'):
    request_parameters_map = {
        'Action' : 'RunInstances',
        'ImageId' : 'ami-02da3a138888ced85',
        'MaxCount' : 1,
        'MinCount' : 1,
        'KeyName' : 'samir-test-key-pair-us-east-1',
        'Version': '2016-11-15'
    }
    request_parameters = urllib.parse.urlencode(request_parameters_map)
    query_request = QueryRequest(
        credentials=credentials,
        method='POST',
        service="ec2",
        host='ec2.amazonaws.com',
        region='us-east-1',
        endpoint='https://ec2.amazonaws.com',
        content_type='application/x-www-form-urlencoded',
        request_parameters=request_parameters
    )
    query_request_handler.performRequest(query_request, region='us-east-1')

def test_describe_instances(credentials, query_request_handler, region='us-east-1'):
    query_request = QueryRequest(
        credentials=credentials,
        method='GET',
        service="ec2",
        host='ec2.amazonaws.com',
        region='us-east-1',
        endpoint='https://ec2.amazonaws.com',
        content_type='application/x-www-form-urlencoded',
        request_parameters='Action=DescribeInstances&Version=2013-10-15'
    )
    query_request_handler.performRequest(query_request)

def test_terminate_instances(credentials, query_request_handler, region='us-east-1'):
    request_parameters_map = {
        'InstanceId.1' : 'i-07185aa5f1e0cf9ac',
        'Action' : 'TerminateInstances',
        'Version': '2016-11-15'
    }
    request_parameters = urllib.parse.urlencode(request_parameters_map)
    query_request = QueryRequest(
        credentials=credentials,
        method='POST',
        service="ec2",
        host='ec2.amazonaws.com',
        region='us-east-1',
        endpoint='https://ec2.amazonaws.com',
        content_type='application/x-www-form-urlencoded',
        request_parameters=request_parameters
    )
    query_request_handler.performRequest(query_request)

def read_credentials():
    with open('credentials.json') as json_file:
        data = json.load(json_file)
        credentials = Credentials(
            access_key=data['access_key'],
            secret_key=data['secret_key']
        )
        return credentials


if __name__ == '__main__':
    credentials = read_credentials()
    query_request_handler = QueryRequestHandler()
    # Uncomment the required lines below to test
    test_describe_regions(credentials, query_request_handler)
    #test_describe_key_pairs(credentials, query_request_handler)
    #test_run_instances(credentials, query_request_handler)
    #test_describe_instances(credentials, query_request_handler)
    #test_terminate_instances(credentials, query_request_handler)
