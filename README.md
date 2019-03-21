# AWS Query Requests

This project contains modular code that will allow users to directly make [AWS Query Requests](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Query-Requests.html) without relying on any particular SDK, and contains all the logic required to digitally sign each request with your AWS keys, using the [Signature 4 Signing Process](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html). This will be useful if you are implementing calls based on the AWS OpenAPI spec ([Sample API spec for EC2](https://api.apis.guru/v2/specs/amazonaws.com/ec2/2016-11-15/swagger.yaml))

## Getting Started

### Project Files
This project consists of 2 parts:
- `aws_query_requests_test.py` - Standalone python program to test signed HTTP requests to the AWS Query Requests API. This internally calls the modular code present in `aws_query_requests.py`
- `AWS Query Requests.ipynb` - Jupyter notebook for testing signed HTTP requests to the AWS Query Requests API using normal HTTP requests as well as boto3 SDK. This notebook is good if you are experimenting with some requests and want to see intermediate outputs.

### Running and Testing
- Create a file named `credentials.json` in the project root directory and save your AWS access key and secret key in it. 
- Run the following command to make signed AWS Query Requests:
	```
	python aws_query_requests_test.py
	```

## Tested APIs
The following API endpoints have been tested for EC2 instances:
- DescribeRegions
- DescribeKeyPairs
- RunInstances
- DescribeInstances
- TerminateInstances

## Useful Links
- https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Operations.html  
- https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html  
- https://docs.aws.amazon.com/AWSEC2/latest/APIReference/Query-Requests.html  
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html?icmpid=docs_ec2_console  
- https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html  
- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html  
