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

class FileServiceCodebuildStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        conf = config.Config(self.node.try_get_context('environment'))
        file_service_repo = conf.get('file_service_repo')
        project_name = conf.get('project_name')
        stage = conf.get('stage')
        application_account_id = conf.get('application_account_id')  
        build_branch = conf.get('build_branch')

        self.file_service_codebuild = codebuild.Project(
            self,
            "FileServiceCodebuild",
            project_name = f"{file_service_repo}-main",
            role = iam.Role.from_role_arn(
                self,
                "FileServiceCodebuildRole",
                role_arn = f"{core.Fn.import_value('CodebuildBeRoleARN')}"
            ),
            source = codebuild.Source.code_commit(
                repository=codecommit.Repository.from_repository_arn(
                    self,
                    "RepoCodebuild",
                    repository_arn = f"{core.Fn.import_value('FileServiceCodeCommitARN')}"
                ),
                branch_or_ref=build_branch
            ),
            logging = codebuild.LoggingOptions(
                cloud_watch = codebuild.CloudWatchLoggingOptions(
                    log_group = logs.LogGroup.from_log_group_arn(
                        self,
                        "FileServiceCodebuildLogGroup",
                        log_group_arn = f"{core.Fn.import_value('LogGroupCodebuildARN')}"
                    )
                ),
                s3 = codebuild.S3LoggingOptions(
                    bucket = s3.Bucket(
                        self,
                        "FileServiceLogBucket",
                        bucket_name=f"{project_name.lower()}-{file_service_repo}-{stage}-build-log"    
                    ),
                    prefix = "build-log"
                )
            )
        )

        core.CfnOutput(self, "FileServiceCodebuildName", value=self.file_service_codebuild.project_name,
                       export_name="FileServiceCodebuildName")
