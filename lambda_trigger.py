import os
import logging
import base64
import boto3
import json
from aws_xray_sdk.core import patch_all
from kube import IOPulseNs, KubeConfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

cognito_idp = boto3.client("cognito-idp")
lambda_client = boto3.client('lambda')


def update_cognito_details(userPoolId, userName, domain):
    cognito_idp.admin_update_user_attributes(
        UserPoolId=userPoolId,
        Username=userName,
        UserAttributes=[{"Name": "custom:domain", "Value": domain}],
    )


def lambda_handler(event, context):
    userPoolId = event.get("userPoolId")
    userName = event.get("userName")
    user_attributes = event.get("request").get("userAttributes")
    email = user_attributes["email"]
    email_url_safe_hash = base64.urlsafe_b64encode(email.encode("utf-8")).decode("utf-8")
    email_url_safe_hash = email_url_safe_hash.lower().replace("=", "")
    kube_config = os.environ['KUBECONFIG']
    kube_role = os.environ["KUBE_ROLE"]
    host_name = os.environ["HOSTNAME"]
    acm_arn = os.environ["ACM_ARN"]
    cluster_name = os.environ["CLUSTER_NAME"]
    lambda_function = os.environ["LAMBDA_FUNCTION"]
    update_cognito_details(userPoolId, userName, f"{email_url_safe_hash}.{host_name}")
    lambda_client.invoke_async(FunctionName=lambda_function, InvokeArgs=json.dumps(event).encode("utf-8"))
    return event
