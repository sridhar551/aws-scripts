import os
import json
import boto3
import logging
import base64

from aws_xray_sdk.core import patch_all


logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

cognito_idp = boto3.client("cognito-idp")

def lambda_handler(event, context):
    try:
        userPoolId = os.environ["USER_POOL_ID"]
        path_parameters = event.get("pathParameters")
        username = path_parameters["username"]
        cognito_idp.admin_delete_user(UserPoolId=userPoolId, Username=username)
        return {
            "statusCode": 200,
            "isBase64Encoded": True,
            "body": json.dumps(
                {"success": True, "data": "User deleted successfully"}
            ),
        }
    except Exception as e:
        return {
            "statusCode": 404,
            "isBase64Encoded": True,
            "body": json.dumps(
                {"success": False, "data": "User does not exist"}
            ),
        }