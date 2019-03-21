import sys
import datetime
import hashlib
import hmac
import requests

class SignatureHelper:
    def __init__(self):
        pass

    def sign(self, key, msg):
        '''
        Key derivation functions. See:
        http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
        '''
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = self.sign(kDate, regionName)
        kService = self.sign(kRegion, serviceName)
        kSigning = self.sign(kService, 'aws4_request')
        return kSigning


class Credentials:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key


class QueryRequest:
    def __init__(self, credentials, method, service, host, region, endpoint, content_type, request_parameters):
        self.credentials = credentials
        self.method = method
        self.service = service
        self.host = host
        self.region = region
        self.endpoint = endpoint
        self.content_type = content_type
        self.request_parameters = request_parameters


class QueryRequestHandler:
    def __init__(self):
        self.amzdate = None
        self.datestamp = None
        self.canonical_request = None
        self.signed_headers = None

    def populateCanonicalInfo(self, query_request):
        # Read AWS access key from env. variables or configuration file. Best practice is NOT
        # to embed credentials in code.
        if query_request.credentials.access_key is None or query_request.credentials.secret_key is None:
            print('No access key is available.')
            sys.exit()

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        self.amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        self.datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        # Step 1 is to define the verb (GET, POST, etc.)--already done.

        # Step 2: Create canonical URI--the part of the URI from domain to query
        # string (use '/' if no path)
        canonical_uri = '/'

        # Step 3: Create the canonical query string. In this example (a GET request),
        # request parameters are in the query string. Query string values must
        # be URL-encoded (space=%20). The parameters must be sorted by name.
        # For this example, the query string is pre-formatted in the request_parameters variable.
        canonical_querystring = query_request.request_parameters if query_request.method == 'GET' else ''
        print("Canonical Query String", canonical_querystring)

        # Step 4: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note that there is a trailing \n.
        canonical_headers = 'content-type:' + query_request.content_type + '\n' \
                            + 'host:' + query_request.host + '\n' \
                            + 'x-amz-date:' + self.amzdate + '\n'

        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        self.signed_headers = 'content-type;host;x-amz-date'

        # Step 6: Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ("").
        payload = ''
        if query_request.method == 'POST':
            payload = query_request.request_parameters
        payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()

        # Step 7: Combine elements to create canonical request
        self.canonical_request = query_request.method + '\n' \
                            + canonical_uri + '\n' \
                            + canonical_querystring + '\n' \
                            + canonical_headers + '\n' \
                            + self.signed_headers + '\n' + payload_hash

    def getAuthorizationHeader(self, query_request):
        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = self.datestamp + '/' + query_request.region + '/' + query_request.service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' \
                         +  self.amzdate + '\n' \
                         +  credential_scope + '\n' \
                         +  hashlib.sha256(self.canonical_request.encode('utf-8')).hexdigest()

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signature_helper = SignatureHelper()
        signing_key = signature_helper.getSignatureKey(query_request.credentials.secret_key, self.datestamp,
                                                       query_request.region, query_request.service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()


        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = algorithm + ' ' \
                               + 'Credential=' + query_request.credentials.access_key + '/' + credential_scope + ', ' \
                               + 'SignedHeaders=' + self.signed_headers + ', ' \
                               + 'Signature=' + signature
        print(authorization_header)
        return authorization_header

    def performRequest(self, query_request):
        self.populateCanonicalInfo(query_request)
        authorization_header = self.getAuthorizationHeader(query_request)

        # The request can include any headers, but MUST include "host", "x-amz-date",
        # and (for this scenario) "Authorization". "host" and "x-amz-date" must
        # be included in the canonical_headers and signed_headers, as noted
        # earlier. Order here is not significant.
        # Python note: The 'host' header is added automatically by the Python 'requests' library.
        headers = {
            'Content-Type': query_request.content_type,
            'x-amz-date': self.amzdate,
            'Authorization': authorization_header
        }
        print("Headers = ", headers)

        # ************* SEND THE REQUEST *************
        print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
        if query_request.method == 'GET':
            request_url = query_request.endpoint + '?' + query_request.request_parameters
            print('Request URL = ' + request_url)
            r = requests.get(request_url, headers=headers)
        elif query_request.method == 'POST':
            request_url = query_request.endpoint
            print('Request URL = ' + request_url)
            r = requests.post(request_url, data=query_request.request_parameters, headers=headers)
        print(r)

        print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        print('Response code: %d\n' % r.status_code)
        print(r.text)