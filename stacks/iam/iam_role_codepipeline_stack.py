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

class IamRoleCodePipelineStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        conf = config.Config(self.node.try_get_context('environment'))
        application_account_id = conf.get('application_account_id')

        # Policy: CodePipelinePolicy
        code_pipeline_policy_document={
            "Statement": [
            {
            "Action": ["iam:PassRole"],
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEqualsIfExists": {
                "iam:PassedToService": [
                    "cloudformation.amazonaws.com",
                    "elasticbeanstalk.amazonaws.com",
                    "ec2.amazonaws.com",
                    "ecs-tasks.amazonaws.com"
                ]
                }
            }
            },
            {
            "Action": [
                "codecommit:CancelUploadArchive",
                "codecommit:GetBranch",
                "codecommit:GetCommit",
                "codecommit:GetRepository",
                "codecommit:GetUploadArchiveStatus",
                "codecommit:UploadArchive"
            ],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": [
                "codedeploy:CreateDeployment",
                "codedeploy:GetApplication",
                "codedeploy:GetApplicationRevision",
                "codedeploy:GetDeployment",
                "codedeploy:GetDeploymentConfig",
                "codedeploy:RegisterApplicationRevision"
            ],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": ["codestar-connections:UseConnection"],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": [
                "elasticbeanstalk:*",
                "ec2:*",
                "elasticloadbalancing:*",
                "autoscaling:*",
                "cloudwatch:*",
                "s3:*",
                "sns:*",
                "cloudformation:*",
                "rds:*",
                "sqs:*",
                "ecs:*"
            ],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": ["lambda:InvokeFunction", "lambda:ListFunctions"],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": [
                "opsworks:CreateDeployment",
                "opsworks:DescribeApps",
                "opsworks:DescribeCommands",
                "opsworks:DescribeDeployments",
                "opsworks:DescribeInstances",
                "opsworks:DescribeStacks",
                "opsworks:UpdateApp",
                "opsworks:UpdateStack"
            ],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:DeleteStack",
                "cloudformation:DescribeStacks",
                "cloudformation:UpdateStack",
                "cloudformation:CreateChangeSet",
                "cloudformation:DeleteChangeSet",
                "cloudformation:DescribeChangeSet",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:SetStackPolicy",
                "cloudformation:ValidateTemplate"
            ],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Action": ["codebuild:BatchGetBuilds", "codebuild:StartBuild"],
            "Resource": "*",
            "Effect": "Allow"
            },
            {
            "Effect": "Allow",
            "Action": [
                "devicefarm:ListProjects",
                "devicefarm:ListDevicePools",
                "devicefarm:GetRun",
                "devicefarm:GetUpload",
                "devicefarm:CreateUpload",
                "devicefarm:ScheduleRun"
            ],
            "Resource": "*"
            },
            {
            "Effect": "Allow",
            "Action": [
                "servicecatalog:ListProvisioningArtifacts",
                "servicecatalog:CreateProvisioningArtifact",
                "servicecatalog:DescribeProvisioningArtifact",
                "servicecatalog:DeleteProvisioningArtifact",
                "servicecatalog:UpdateProduct"
            ],
            "Resource": "*"
            },
            {
            "Effect": "Allow",
            "Action": ["cloudformation:ValidateTemplate"],
            "Resource": "*"
            },
            {
            "Effect": "Allow",
            "Action": ["ecr:DescribeImages"],
            "Resource": "*"
            }
        ],
        "Version": "2012-10-17"
        }

        custom_code_pipeline_policy_document = iam.PolicyDocument.from_json(code_pipeline_policy_document)

        self.code_pipeline_policy = iam.ManagedPolicy(
            self,
            "CodePipelinePolicy",
            document=custom_code_pipeline_policy_document,
            managed_policy_name="Codepipeline-policy", 
            path="/",
        )

        self.code_pipeline_policy_arn =  self.code_pipeline_policy.managed_policy_arn

        self.code_pipeline_role = iam.Role(
            self,
            "CodePipelineRole",
            assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
            role_name="CodePipeline-role"
        )

        self.code_pipeline_role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self, 
            "CodePipelineRoleAssignedPolicy", 
            f"{self.code_pipeline_policy_arn}"
            )
        )

        core.CfnOutput(self, "CodePipelineRoleARN", value=self.code_pipeline_role.role_arn,
                       export_name="CodePipelineRoleARN")



