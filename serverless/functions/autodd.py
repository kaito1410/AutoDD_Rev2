import json


def autodd(event, context):
    body = {
        "message": "Hello AutoDD from lambda!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
