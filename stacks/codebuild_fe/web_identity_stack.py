from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_codecommit as codecommit,
    aws_iam as iam,
    aws_s3 as s3,
    aws_codebuild as codebuild,
    aws_cloudformation as cfn,
    aws_logs as logs,
)
from constructs import Construct
import aws_cdk as core
from helper import config

class WebIdentityCodebuildStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        conf = config.Config(self.node.try_get_context('environment'))
        web_identity_repo = conf.get('web_identity_repo')
        project_name = conf.get('project_name')
        stage = conf.get('stage')
        application_account_id = conf.get('application_account_id')  
        build_branch = conf.get('build_branch')

        self.log_group = logs.LogGroup(
            self,
            "WebIdentityCodebuildLogGroup",
            log_group_name = "log-group"
        )

        self.log_group.add_stream(
            "WebIdentityCodebuildLogStream",
            log_stream_name = "log-stream"
        )

        core.CfnOutput(self, "LogGroupCodebuildName", value=self.log_group.log_group_name,
                       export_name="LogGroupCodebuildName")
        core.CfnOutput(self, "LogGroupCodebuildARN", value=self.log_group.log_group_arn,
                       export_name="LogGroupCodebuildARN")

        self.web_identity_codebuild = codebuild.Project(
            self,
            "WebIdentityCodebuild",
            project_name = f"{web_identity_repo}-main",
            role = iam.Role.from_role_arn(
                self,
                "WebIdentityCodebuildRole",
                role_arn = f"{core.Fn.import_value('CodebuildFeRoleARN')}"
            ),
            source = codebuild.Source.code_commit(
                repository=codecommit.Repository.from_repository_arn(
                    self,
                    "WebIdentityRepoCodebuild",
                    repository_arn = f"{core.Fn.import_value('WebIdentityCodeCommitARN')}"
                ),
                branch_or_ref=build_branch
            ),
            logging = codebuild.LoggingOptions(
                cloud_watch = codebuild.CloudWatchLoggingOptions(
                    # log_group = self.log_group.add_stream(
                    #     "WebIdentityCodebuildLogStream",
                    #     log_stream_name = "log-stream"
                    # ),

                    log_group = self.log_group
                ),
                s3 = codebuild.S3LoggingOptions(
                    bucket = s3.Bucket(
                        self,
                        "WebIdentityLogBucket",
                        bucket_name=f"{project_name.lower()}-{web_identity_repo}-{stage}-build-log"    
                    ),
                    prefix = "build-log"
                )
            )
        )

        core.CfnOutput(self, "WebIdentityCodebuildName", value=self.web_identity_codebuild.project_name,
                       export_name="WebIdentityCodebuildName")
        core.CfnOutput(self, "WebIdentityCodebuildARN", value=self.web_identity_codebuild.project_arn,
                       export_name="WebIdentityCodebuildARN")
