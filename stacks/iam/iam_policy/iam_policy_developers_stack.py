import json

from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as core
from stacks.iam.iam_group_stack import IamGroupStack
from helper import config

class IamPolicyDevelopersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        conf = config.Config(self.node.try_get_context('environment'))
        account_id = conf.get('account_id')
        iam_group_stack = IamGroupStack(self, "iam-policy-stack")
        developers_policy_document={
            "Statement": [
                {
                    "Action": [
                        "codecommit:Update*",
                        "codecommit:Merge*",
                        "codecommit:Post*",
                        "codecommit:Get*",
                        "codecommit:Test*",
                        "codecommit:BatchGet*",
                        "codecommit:GitPull",
                        "codecommit:Create*",
                        "codecommit:List*",
                        "codecommit:Describe*",
                        "codecommit:Put*",
                        "codecommit:GitPush"
                    ],
                    "Effect": "Allow",
                    "Resource": "*",
                    "Sid": "AllowPull"
                },
                {
                    "Action": [
                        "codecommit:PutFile",
                        "codecommit:GitPush",
                        "codecommit:DeleteBranch",
                        "codecommit:Merge*"
                    ],
                    "Condition": {
                        "Null": {
                            "codecommit:References": "false"
                        },
                        "StringEqualsIfExists": {
                            "codecommit:References": [
                                "refs/heads/main",
                                "refs/heads/master",
                                "refs/heads/uat",
                                "refs/heads/develop",
                                "refs/heads/qa",
                                "refs/heads/test"
                            ]
                        }
                    },
                    "Effect": "Deny",
                    "Resource": "arn:aws:codecommit:us-west-2:894126404273:*",
                    "Sid": "DenyPush"
                }
            ],
            "Version": "2012-10-17"
        }

        custom_developers_policy_document = iam.PolicyDocument.from_json(developers_policy_document)

        self.Developers_managed_policy = iam.CfnManagedPolicy(
            self,
            "DevelopersPolicy",
            policy_document=custom_developers_policy_document,
            groups=[iam_group_stack.Developers_group.group_name],
            managed_policy_name="CodeCommit-Policies-Devs", 
            path="/",
        )




