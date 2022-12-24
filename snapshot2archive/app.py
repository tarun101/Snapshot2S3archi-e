import json
import boto3
from datetime import date

ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    snapshots = ec2.describe_snapshots(
        Filters=[{
            'Name': 'owner-id',
            'Values': ['YOUR_OWNER_ID'],
        },
            {
            'Name': 'storage-tier',
            'Values': ['standard'],
        },
        ])

    for snapshot in snapshots['Snapshots']:
        if snapshot['StartTime'].date() < date.today()-90:
            response = ec2.modify_snapshot_tier(
                SnapshotId=snapshot['SnapshotId'],
                StorageTier='archive'
            )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Success",
        }),
    }