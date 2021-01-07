import os
import logging
import boto3
import base64
import json
from aws_xray_sdk.core import patch_all
from kube import IOPulseNs, KubeConfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

cognito_idp = boto3.client("cognito-idp")

def lambda_handler(event, context):

    try:
        userPoolId = os.environ["USER_POOL_ID"]
        path_parameters = event.get("pathParameters")
        username = path_parameters["username"]
        get_user = cognito_idp.admin_get_user(UserPoolId=userPoolId, Username=username)
        namespace = get_user['UserAttributes'][2]['Value'].split('.')[0]
        kube_config = os.environ['KUBECONFIG']
        cluster_name = os.environ["CLUSTER_NAME"]
        conf = KubeConfig(cluster_name=cluster_name, kube_filepath=kube_config, role=None)
        conf.read_eks_cluster_details()
        iopulse = IOPulseNs(name=namespace,userId="", email="", kube_filepath=kube_config)
        congito_response = cognito_idp.admin_delete_user(UserPoolId=userPoolId, Username=username)
        if congito_response:
            response = iopulse.delete_namespace()
            return {
                "statusCode": 200,
                "isBase64Encoded": False,
                "body": json.dumps(
                    {"success": True, "data": "namespace and cognito user has deleted"}
                ),
            }
        # else:
        #     return {
        #         "statusCode": 200,
        #         "isBase64Encoded": False,
        #         "body": json.dumps(
        #             {"success": True, "data": "namespace or congnito user is not exist"}
        #         ),
        #     }
    except Exception as e:
        return {
            "statusCode": 404,
            "isBase64Encoded": False,
            "body": json.dumps(
                {"success": False, "data": str(e)}
            ),
        }