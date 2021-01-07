import os
import logging
import base64
from aws_xray_sdk.core import patch_all
from kube import IOPulseNs, KubeConfig

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


def lambda_handler(event, context):
    user_attributes = event.get("request").get("userAttributes")
    email = user_attributes["email"]
    username = event.get("userName")
    email_url_safe_hash = base64.urlsafe_b64encode(email.encode("utf-8")).decode("utf-8")
    email_url_safe_hash = email_url_safe_hash.lower().replace("=", "")
    kube_config = os.environ['KUBECONFIG']
    kube_role = os.environ["KUBE_ROLE"]
    host_name = os.environ["HOSTNAME"]
    acm_arn = os.environ["ACM_ARN"]
    deployment_repo_name = os.environ["DEPLOYMENT_ECR_NAME"]
    cluster_name = os.environ["CLUSTER_NAME"]
    conf = KubeConfig(cluster_name=cluster_name, kube_filepath=kube_config, role=None)
    conf.read_eks_cluster_details()
    iopulse = IOPulseNs(name=email_url_safe_hash,userId=username, email=email, kube_filepath=kube_config)
    iopulse.update_deployment(image=deployment_repo_name, port=1880)
    return event

if __name__ == '__main__':
    config = KubeConfig(cluster_name="krysp-eks")
    iopulse = IOPulseNs(name="dmfzds50aglydxzlzwr1qgzpc3npb25sywjzlmnvbq", userId="", email="", kube_filepath=None)
    response = iopulse.update_deployment(image=deployment_repo_name, port=1880)
    print(response)