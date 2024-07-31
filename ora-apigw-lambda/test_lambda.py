from lambda_function import lambda_handler

apigw_event = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/conversations",
    "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
    "cookies": [],
    "headers": {"Header1": "value1", "Header2": "value1,value2"},
    "queryStringParameters": {"parameter1": "value1,value2", "parameter2": "value"},
    "requestContext": {
        "accountId": "123456789012",
        "apiId": "api-id",
        "authentication": {
            "clientCert": {
                "clientCertPem": "CERT_CONTENT",
                "subjectDN": "www.example.com",
                "issuerDN": "Example issuer",
                "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                "validity": {
                    "notBefore": "May 28 12:30:02 2019 GMT",
                    "notAfter": "Aug  5 09:36:04 2021 GMT",
                },
            }
        },
        "domainName": "id.execute-api.us-east-1.amazonaws.com",
        "domainPrefix": "id",
        "http": {
            "method": "POST",
            "path": "/conversations",
            "protocol": "HTTP/1.1",
            "sourceIp": "192.168.0.1/32",
            "userAgent": "agent",
        },
        "requestId": "id",
        "routeKey": "$default",
        "stage": "$default",
        "time": "12/Mar/2020:19:03:58 +0000",
        "timeEpoch": 1583348638390,
    },
    "body": '{"message": "Oh, I see. But I have thought you are Ora, my mental health supporter.", "user_id": "c33195e9-6865-4902-bd5b-c868a9dc4fbf"}',
}

result = lambda_handler(apigw_event, {})
print(result)
