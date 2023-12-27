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

class FileServiceCodecommitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        conf = config.Config(self.node.try_get_context('environment'))
        file_service_repo = conf.get('file_service_repo')

        # Repo: file-service
        self.file_service_repo = codecommit.Repository(
            self, 
            f"{file_service_repo}",
            repository_name=f"{file_service_repo}",
        )

        self.file_service_repo.default_branch = "develop"
        
        self.file_service_arn = self.file_service_repo.repository_arn
        
        file_service_codecommit_policy_document={
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
                "Resource": f"{self.file_service_arn}",
                "Condition": {
                    "StringNotEquals": {
                    "codecommit:References": ["refs/heads/main", "refs/heads/master"]
                    }
                }
                }
            ]
        }

        custom_file_service_codecommit_policy_document = iam.PolicyDocument.from_json(file_service_codecommit_policy_document)

        self.file_service_codecommit_policy = iam.CfnManagedPolicy(
            self,
            "FileServiceCodeCommitPolicy",
            policy_document=custom_file_service_codecommit_policy_document,
            managed_policy_name=f"CodeCommit-Policies-Backend-{file_service_repo}", 
            path="/",
        )

        # Output
        core.CfnOutput(self, "FileServiceCodeCommitARN", value=self.file_service_repo.repository_arn,
                       export_name="FileServiceCodeCommitARN")
