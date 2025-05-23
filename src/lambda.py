import boto3
from custom import generate_presigned_url

def lambda_handler(event, context):
    client = boto3.client('lambda')
    layers_info = []

    paginator = client.get_paginator('list_layers')
    for page in paginator.paginate():
        for layer in page.get('Layers', []):
            layer_name = layer['LayerName']
            latest_version_arn = layer['LatestMatchingVersion']['LayerVersionArn']
            layers_info.append({
                'layer_name': layer_name,
                'latest_version_arn': latest_version_arn
            })

    return {
        'statusCode': 200,
        'body': layers_info
    }
