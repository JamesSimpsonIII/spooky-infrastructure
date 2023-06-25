from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    RemovalPolicy,
    # aws_sqs as sqs,
)
from constructs import Construct

class SpookyInfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "SpookyInfrastructureQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        table = dynamodb.Table(self, "Spooky Quotes", 
            partition_key={"name": "id", "type": dynamodb.AttributeType.NUMBER},
            removal_policy=RemovalPolicy.DESTROY
        )

        function = lambda_.Function(self, "getQuotes", 
            code=lambda_.Code.from_asset("lambda"),
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="handler.handler",
            environment= {
                "TABLE_NAME": table.table_name
            }
        )

        table.grant_read_write_data(function)

        endpoint = apigw.LambdaRestApi(self, "Quotes Endpoint",
            handler=function,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            )
        )

        
