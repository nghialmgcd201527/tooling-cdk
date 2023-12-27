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

class WebComponentCodecommitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        conf = config.Config(self.node.try_get_context('environment'))
        web_component_repo = conf.get('web_component_repo')

        # Repo: web-component
        self.web_component_repo = codecommit.Repository(
            self, 
            f"{web_component_repo}",
            repository_name=f"{web_component_repo}",
        )

        self.web_component_repo.default_branch = "develop"
        
        self.web_component_arn = self.web_component_repo.repository_arn
        
        web_component_codecommit_policy_document={
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
                "Resource": f"{self.web_component_arn}",
                "Condition": {
                    "StringNotEquals": {
                    "codecommit:References": ["refs/heads/main", "refs/heads/master"]
                    }
                }
                }
            ]
        }

        custom_web_component_codecommit_policy_document = iam.PolicyDocument.from_json(web_component_codecommit_policy_document)

        self.web_component_codecommit_policy = iam.CfnManagedPolicy(
            self,
            "WebComponentCodeCommitPolicy",
            policy_document=custom_web_component_codecommit_policy_document,
            managed_policy_name=f"CodeCommit-Policies-Frontend-{web_component_repo}", 
            path="/",
        )

        # Output
        core.CfnOutput(self, "WebComponentCodeCommitFE", value=self.web_component_repo.repository_arn,
                       export_name="WebComponentCodeCommitFE")

        # self.web_identity_repo = codecommit.CfnRepository(
        #     self,
        #     f"{web_identity_repo}",
        #     repository_name=f"{web_identity_repo}",
        #     code = codecommit.CfnRepository.CodeProperty(
        #         s3=codecommit.CfnRepository.S3Property(
        #             bucket=f"code-commit-{web_identity_repo}",
        #             key=f"{web_identity_repo}",
        #         ),
        #         branch_name="develop",
        #     )
        # )