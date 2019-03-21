from aws_query_requests import Credentials, QueryRequest, QueryRequestHandler
import urllib

query_request_handler = QueryRequestHandler()
credentials = Credentials(
    access_key='<ACCESS_KEY>',
    secret_key='<SECRET_KEY>'
)

def test_describe_regions():
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

def test_describe_key_pairs():
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

def test_run_instances():
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
    query_request_handler.performRequest(query_request)

def test_describe_instances():
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

def test_terminate_instances():
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

if __name__ == '__main__':
    test_describe_regions()
    #test_describe_key_pairs()
    #test_run_instances()
    #test_describe_instances()
    #test_terminate_instances()
