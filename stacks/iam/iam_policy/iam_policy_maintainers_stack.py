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

class IamPolicyMaintainersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        conf = config.Config(self.node.try_get_context('environment'))
        account_id = conf.get('account_id')
        iam_group_stack = IamGroupStack(self, "iam-policy-stack")
        maintainers_policy_document={
            "Statement": [
                {
                    "Action": [
                        "codecommit:Merge*",
                        "codecommit:TagResource",
                        "codecommit:BatchAssociateApprovalRuleTemplateWithRepositories",
                        "codecommit:BatchGet*",
                        "codecommit:GitPull",
                        "codecommit:UntagResource",
                        "codecommit:BatchDisassociateApprovalRuleTemplateFromRepositories",
                        "codecommit:OverridePullRequestApprovalRules",
                        "codecommit:Post*",
                        "codecommit:EvaluatePullRequestApprovalRules",
                        "codecommit:Test*",
                        "codecommit:DisassociateApprovalRuleTemplateFromRepository",
                        "codecommit:Describe*",
                        "codecommit:Put*",
                        "codecommit:GitPush",
                        "codecommit:DeleteFile",
                        "codecommit:BatchDescribe*",
                        "codecommit:AssociateApprovalRuleTemplateWithRepository",
                        "codecommit:Update*",
                        "codecommit:Get*",
                        "codecommit:Create*",
                        "codecommit:List*"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:codecommit:us-west-2:625249961471:*",
                    "Sid": "MainPermission"
                },
                {
                    "Action": "codecommit:DeleteBranch",
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
                    "Sid": "PreventDeleteBranch"
                }
            ],
            "Version": "2012-10-17"
        }

        custom_maintainers_policy_document = iam.PolicyDocument.from_json(maintainers_policy_document)

        self.Maintainers_managed_policy = iam.CfnManagedPolicy(
            self,
            "MaintainersPolicy",
            policy_document=custom_maintainers_policy_document,
            groups=[iam_group_stack.Maintainers_group.group_name],
            managed_policy_name="CodeCommit-Policies-Maintainers", 
            path="/",
        )




