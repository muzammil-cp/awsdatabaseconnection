import os
import sys
import boto3
from botocore.exceptions import ClientError

# Read the region from environment variables (defaults to eu-north-1 to match your console)
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "eu-north-1")

# Connect to the live AWS DynamoDB Service
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
TABLE_NAME = "dynamodb"


def setup_table():
    """Creates the table in AWS if it does not already exist."""
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        print(f"Creating live AWS table '{TABLE_NAME}' in {AWS_REGION}... Please wait.")
        table.wait_until_exists()
        print(f"Table '{TABLE_NAME}' is now active on AWS!")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Table '{TABLE_NAME}' already exists in {AWS_REGION}. Proceeding...")
        else:
            print(f"AWS Error: {e.response['Error']['Message']}")
            sys.exit(1)


def main():
    setup_table()
    table = dynamodb.Table(TABLE_NAME)

    try:
        # 1. PUT data into AWS DynamoDB
        print("\n--- Putting Data to AWS ---")
        item_data = {"id": 789, "name": "John Doe", "status": "Active"}
        table.put_item(Item=item_data)
        print(f"Successfully saved item: {item_data}")

        # 2. GET data back from AWS DynamoDB
        print("\n--- Getting Data from AWS ---")
        response = table.get_item(Key={"id": 789})

        if "Item" in response:
            print(f"Successfully retrieved item from AWS: {response['Item']}")
        else:
            print("Item not found on AWS.")
    except ClientError as e:
        print(f"AWS Operation Error: {e.response['Error']['Message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()