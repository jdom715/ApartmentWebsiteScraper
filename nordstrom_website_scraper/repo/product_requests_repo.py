# coding=utf-8
import boto3
from botocore.exceptions import ClientError

_dynamodb: boto3 = boto3.resource("dynamodb", region_name="us-west-2", endpoint_url="http://localhost:8000")
_product_requests_table = _dynamodb.Table("product-requests")


def get_product_requests():
    try:
        _product_requests_table.scan()
    except ClientError as e:
        print(e.response["Error"]["Message"])
