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

class IamPolicyDevopsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        conf = config.Config(self.node.try_get_context('environment'))
        account_id = conf.get('account_id')
        iam_group_stack = IamGroupStack(self, "iam-policy-stack")
        devops_policy_document={
            "Statement": [
                {
                    "Action": [
                        "codecommit:GitPull",
                        "codecommit:Get*",
                        "codecommit:List*"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:codecommit:us-west-2:625249961471:*",
                    "Sid": "GeneralPermissionsDevOps"
                },
                {
                    "Action": [
                        "codecommit:BatchGet*",
                        "codecommit:BatchDescribe*",
                        "codecommit:Create*",
                        "codecommit:DeleteFile",
                        "codecommit:Describe*",
                        "codecommit:List*",
                        "codecommit:Merge*",
                        "codecommit:OverridePullRequestApprovalRules",
                        "codecommit:Put*",
                        "codecommit:Post*",
                        "codecommit:TagResource",
                        "codecommit:Test*",
                        "codecommit:UntagResource",
                        "codecommit:Update*",
                        "codecommit:GitPush"
                    ],
                    "Condition": {
                        "StringNotEquals": {
                            "codecommit:References": [
                                "refs/heads/main",
                                "refs/heads/master"
                            ]
                        }
                    },
                    "Effect": "Allow",
                    "Resource": "arn:aws:codecommit:us-west-2:625249961471:*",
                    "Sid": "SpecificPermissionForDevOps"
                }
            ],
            "Version": "2012-10-17"
        }

        custom_devops_policy_document = iam.PolicyDocument.from_json(devops_policy_document)

        self.DevOps_managed_policy = iam.CfnManagedPolicy(
            self,
            "DevOpsPolicy",
            policy_document=custom_devops_policy_document,
            groups=[iam_group_stack.DevOps_group.group_name],
            managed_policy_name="CodeCommit-Policies-DevOps", 
            path="/",
        )




