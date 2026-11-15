## Run the DynamoDB demo

The app uses the AWS SDK default credential chain. Do not put AWS access keys in the Docker command or commit them to Git.

### Recommended on EC2

Attach an IAM instance role to the EC2 instance with the DynamoDB permissions below. The container can then use the role automatically:

```bash
docker run --rm -e AWS_DEFAULT_REGION=eu-north-1 febnotechkolkata/aws-dynamo-app
```

### Run locally with an AWS CLI profile

First sign in or configure an AWS CLI profile on your computer. Then mount its credentials read-only into the container:

```bash
docker run --rm -e AWS_DEFAULT_REGION=eu-north-1 -e AWS_PROFILE=default -v "$HOME/.aws:/root/.aws:ro" febnotechkolkata/aws-dynamo-app
```

In PowerShell, use `-v "$env:USERPROFILE\.aws:/root/.aws:ro"` instead of the Linux/macOS volume argument.

The IAM role or profile needs `dynamodb:CreateTable`, `dynamodb:DescribeTable`, `dynamodb:PutItem`, and `dynamodb:GetItem` on the demo table. The app creates a provisioned table named `dynamodb` in the selected region and writes a sample item. DynamoDB provisioned capacity can incur AWS charges; delete the demo table when you no longer need it.
