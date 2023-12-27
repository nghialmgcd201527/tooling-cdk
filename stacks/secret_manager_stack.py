from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_secretsmanager as secretsmanager,
    SecretValue as SecretValue,
)
from constructs import Construct
import aws_cdk as core
from helper import config

class SecretManagerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        conf = config.Config(self.node.try_get_context('environment'))
        environment = conf.get('environment')
        stage = conf.get('stage')

        self.secret_manager = secretsmanager.Secret(
            self, 
            f'{environment}_Secret',
            secret_name=f'{environment}_Secret',
            secret_object_value={
                "test": SecretValue.unsafe_plain_text("test"),
            }
        )

        core.CfnOutput(self, f"{stage}SecretARN", value=self.secret_manager.secret_arn,
                       export_name=f"{stage}SecretARN")
