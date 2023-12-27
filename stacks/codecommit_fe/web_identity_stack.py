from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_codecommit as codecommit,
    aws_iam as iam,
)
from constructs import Construct
import aws_cdk as core
from helper import config

class WebIdentityCodecommitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        conf = config.Config(self.node.try_get_context('environment'))
        web_identity_repo = conf.get('web_identity_repo')

        # Repo: web-identity
        self.web_identity_repo = codecommit.Repository(
            self, 
            f"{web_identity_repo}",
            repository_name=f"{web_identity_repo}",
        )

        self.web_identity_repo.default_branch = "develop"
        
        self.web_identity_arn = self.web_identity_repo.repository_arn
        
        web_identity_codecommit_policy_document={
            "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Action": [
                    "codecommit:BatchGet*",
                    "codecommit:Get*",
                    "codecommit:List*",
                    "codecommit:Create*",
                    "codecommit:Describe*",
                    "codecommit:Put*",
                    "codecommit:Post*",
                    "codecommit:Merge*",
                    "codecommit:Test*",
                    "codecommit:Update*",
                    "codecommit:GitPull",
                    "codecommit:GitPush"
                ],
                "Resource": "*"
                },
                {
                "Sid": "SpecificPermissionForDev",
                "Effect": "Allow",
                "Action": [
                    "codecommit:GitPush",
                    "codecommit:DeleteBranch",
                    "codecommit:PutFile",
                    "codecommit:Merge*"
                ],
                "Resource": f"{self.web_identity_arn}",
                "Condition": {
                    "StringNotEquals": {
                    "codecommit:References": ["refs/heads/main", "refs/heads/master"]
                    }
                }
                }
            ]
        }

        custom_web_identity_codecommit_policy_document = iam.PolicyDocument.from_json(web_identity_codecommit_policy_document)

        self.web_identity_codecommit_policy = iam.CfnManagedPolicy(
            self,
            "WebIdentityCodeCommitPolicy",
            policy_document=custom_web_identity_codecommit_policy_document,
            managed_policy_name=f"CodeCommit-Policies-Frontend-{web_identity_repo}", 
            path="/",
        )

        # Output
        core.CfnOutput(self, "WebIdentityCodeCommitARN", value=self.web_identity_repo.repository_arn,
                       export_name="WebIdentityCodeCommitARN")
        core.CfnOutput(self, "WebIdentityCodeCommitName", value=self.web_identity_repo.repository_name,
                       export_name="WebIdentityCodeCommitName")
