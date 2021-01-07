import os
import logging
import base64
import json
from aws_xray_sdk.core import patch_all
from kube import IOPulseNs, KubeConfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


def lambda_handler(event, context):
    try:
        path_parameters = event.get("pathParameters")
        namespace = path_parameters["namespace"]
        kube_config = os.environ['KUBECONFIG']
        cluster_name = os.environ["CLUSTER_NAME"]
        conf = KubeConfig(cluster_name=cluster_name, kube_filepath=kube_config, role=None)
        conf.read_eks_cluster_details()
        iopulse = IOPulseNs(name = namespace ,userId="", email="", kube_filepath=kube_config)
        response = iopulse.delete_pod()
        return {
            'statusCode': 200,
            'body': json.dumps(
                {"success": True}
            ),
        }
    except Exception as e:
        return {
            "statusCode": 404,
            "isBase64Encoded": False,
            "body": json.dumps(
                {"success": False, "data": str(e)}
            ),
        }