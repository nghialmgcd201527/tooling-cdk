import json

from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as core
from helper import config

class IamRoleCodebuildBeStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        conf = config.Config(self.node.try_get_context('environment'))
        application_account_id = conf.get('application_account_id')

        # Policy: AllowToAssumeCodeArtifact
        allow_to_assume_code_artifact_document={
            "Version": "2012-10-17",
            "Statement": [
                {
                "Sid": "AllowToAccessPuraVidaCodeArtifact",
                "Effect": "Allow",
                "Resource": ["arn:aws:iam::894126404273:role/CrossAccountCodeArtirfact"],
                "Action": "sts:AssumeRole"
                }
            ]
        }

        custom_allow_to_assume_code_artifact_document = iam.PolicyDocument.from_json(allow_to_assume_code_artifact_document)

        self.allow_to_assume_code_artifact_policy = iam.ManagedPolicy(
            self,
            "AllowToAssumeCodeArtifactPolicy",
            document=custom_allow_to_assume_code_artifact_document,
            managed_policy_name="AllowToAssumeCodeArtifactBe", 
            path="/",
        )

        # Policy: AllowToAssumeApplication
        allow_to_assume_application_document={
            "Version": "2012-10-17",
            "Statement": [
                {
                "Sid": "AllowCodeBuildToAccessApplication",
                "Effect": "Allow",
                "Resource": [
                    f"arn:aws:iam::{application_account_id}:role/Cross-Account-Code-Build-Role"
                ],
                "Action": "sts:AssumeRole"
                }
            ]
        }

        custom_allow_to_assume_application_document = iam.PolicyDocument.from_json(allow_to_assume_application_document)

        self.allow_to_assume_application_policy = iam.ManagedPolicy(
            self,
            "AllowToAssumeApplicationPolicy",
            document=custom_allow_to_assume_application_document,
            managed_policy_name="AllowToAssumeApplicationBe", 
            path="/",
        )

        # Policy: CodeBuild-execution-role-policy
        codebuild_execution_role_document={
            "Statement": [
                {
                    "Action": "secretsmanager:GetSecretValue",
                    "Effect": "Allow",
                    "Resource": "*",
                    "Sid": "EnableToReadTheSecret"
                },
                {
                    "Action": "ssm:*",
                    "Effect": "Allow",
                    "Resource": "*"
                },
                {
                    "Action": [
                        "s3:ListBucket"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::*"
                },
                {
                    "Action": [
                        "s3:DeleteObject",
                        "s3:GetObject",
                        "s3:GetObjectAcl",
                        "s3:ListBucket",
                        "s3:PutObject",
                        "s3:PutObjectAcl"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:s3:::*/*",
                        "arn:aws:s3:::*"
                    ]
                },
                {
                    "Action": [
                        "codeartifact:GetAuthorizationToken",
                        "codeartifact:GetRepositoryEndpoint",
                        "codeartifact:ReadFromRepository"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                },
                {
                    "Action": "sts:GetServiceBearerToken",
                    "Condition": {
                        "StringEquals": {
                            "sts:AWSServiceName": "codeartifact.amazonaws.com"
                        }
                    },
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ],
            "Version": "2012-10-17"
        }

        custom_codebuild_execution_role_document = iam.PolicyDocument.from_json(codebuild_execution_role_document)

        self.codebuild_execution_role_policy = iam.ManagedPolicy(
            self,
            "CodebuildExecutionRolePolicy",
            document=custom_codebuild_execution_role_document,
            managed_policy_name="CodeBuild-execution-role-policyBe", 
            path="/",
        )

        # Policy: CodeBuildbase-policy
        codebuild_base_document={
            "Statement": [
                {
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Action": [
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:GetObjectVersion",
                        "s3:GetBucketAcl",
                        "s3:GetBucketLocation"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:s3:::codepipeline-us-west-2-*"
                    ]
                },
                {
                    "Action": [
                        "codecommit:GitPull",
                        "codecommit:GitPush"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:codecommit:us-west-2:*"
                    ]
                },
                {
                    "Action": [
                        "codebuild:CreateReportGroup",
                        "codebuild:CreateReport",
                        "codebuild:UpdateReport",
                        "codebuild:BatchPutTestCases",
                        "codebuild:BatchPutCodeCoverages"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:codebuild:us-west-2:*"
                    ]
                },
                {
                    "Action": [
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:BatchGetImage",
                        "ecr:DescribeImages",
                        "ecr:GetAuthorizationToken",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:InitiateLayerUpload",
                        "ecr:CompleteLayerUpload",
                        "ecr:PutImage",
                        "ecr:UploadLayerPart",
                        "ec2:*"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ],
            "Version": "2012-10-17"
        }

        custom_codebuild_base_document = iam.PolicyDocument.from_json(codebuild_base_document)

        self.codebuild_base_policy = iam.ManagedPolicy(
            self,
            "CodebuildBasePolicy",
            document=custom_codebuild_base_document,
            managed_policy_name="CodeBuildbase-policyBe", 
            path="/",
        )
        
        self.allow_to_assume_code_artifact_policy_arn =  self.allow_to_assume_code_artifact_policy.managed_policy_arn
        self.allow_to_assume_application_policy_arn =  self.allow_to_assume_application_policy.managed_policy_arn
        self.codebuild_execution_role_policy_arn =  self.codebuild_execution_role_policy.managed_policy_arn
        self.codebuild_base_policy_arn =  self.codebuild_base_policy.managed_policy_arn

        self.codebuild_role_for_code_artifact = iam.Role(
            self,
            "CodebuildBeRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            role_name="Codebuild-role"
        )

        self.codebuild_role_for_code_artifact.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self, 
            "AllowToAssumeCodeArtifactAssignedRoleBe", 
            f"{self.allow_to_assume_code_artifact_policy_arn}"
            )
        )

        self.codebuild_role_for_code_artifact.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self, 
            "AllowToAssumeApplicationAssignedRoleBe", 
            f"{self.allow_to_assume_application_policy_arn}"
            )
        )

        self.codebuild_role_for_code_artifact.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self, 
            "CodebuildExecutionRolePolicyAssignedRoleBe", 
            f"{self.codebuild_execution_role_policy_arn}"
            )
        )

        self.codebuild_role_for_code_artifact.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self, 
            "CodebuildBasePolicyAssignedRoleBe", 
            f"{self.codebuild_base_policy_arn}"
            )
        )

        core.CfnOutput(self, "CodebuildBeRoleARN", value=self.codebuild_role_for_code_artifact.role_arn,
                       export_name="CodebuildBeRoleARN")
        core.CfnOutput(self, "CodebuildBeRoleID", value=self.codebuild_role_for_code_artifact.role_id,
                       export_name="CodebuildBeRoleID")
        core.CfnOutput(self, "CodebuildBeRoleName", value=self.codebuild_role_for_code_artifact.role_name,
                       export_name="CodebuildBeRoleName")



