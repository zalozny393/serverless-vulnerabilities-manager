import json


def response(data, status=200):
    return {"statusCode": status, "body": json.dumps(data)}
