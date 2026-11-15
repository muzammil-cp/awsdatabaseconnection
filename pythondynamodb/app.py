import os
import sys

import boto3
from botocore.exceptions import ClientError

AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-north-1")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "dynamodb")
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


def setup_table():
    """Create the demo table if needed and wait until it is ready."""
    table = dynamodb.Table(TABLE_NAME)
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        print(f"Creating DynamoDB table {TABLE_NAME!r} in {AWS_REGION}; waiting for it to become active.")
    except ClientError as error:
        if error.response.get("Error", {}).get("Code") != "ResourceInUseException":
            print(f"Could not create DynamoDB table: {error}", file=sys.stderr)
            sys.exit(1)
        print(f"DynamoDB table {TABLE_NAME!r} already exists; waiting until it is active.")

    try:
        table.wait_until_exists()
        print(f"DynamoDB table {TABLE_NAME!r} is active in {AWS_REGION}.")
    except ClientError as error:
        print(f"Could not wait for DynamoDB table: {error}", file=sys.stderr)
        sys.exit(1)


def main():
    setup_table()
    table = dynamodb.Table(TABLE_NAME)

    try:
        print("\n--- Putting data into DynamoDB ---")
        item_data = {"id": 789, "name": "John Doe", "status": "Active"}
        table.put_item(Item=item_data)
        print(f"Saved item: {item_data}")

        print("\n--- Getting data from DynamoDB ---")
        response = table.get_item(Key={"id": 789})
        if "Item" in response:
            print(f"Retrieved item: {response['Item']}")
        else:
            print("Item not found.")
    except ClientError as error:
        print(f"DynamoDB operation failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
