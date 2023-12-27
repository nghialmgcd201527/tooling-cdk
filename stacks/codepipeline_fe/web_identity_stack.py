from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codecommit as codecommit,
    aws_codebuild as codebuild,
    aws_events as events,
    aws_iam as iam,
    aws_events_targets as events_targets,
)
from constructs import Construct
import aws_cdk as core
from helper import config

class WebIdentityCodePipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        conf = config.Config(self.node.try_get_context('environment'))
        stage = conf.get('stage')
        project_name = conf.get('project_name')
        web_identity_repo = conf.get('web_identity_repo')
        branch = conf.get('default_branch')
        account_id = conf.get('account_id')

        self.web_identity_codepipeline = codepipeline.Pipeline(
            self,
            "WebIdentityCodePipeline",
            artifact_bucket = s3.Bucket(
                self,
                "WebIdentityCodePipelineLogBucket",
                bucket_name=f"{project_name.lower()}-{web_identity_repo}-{stage}-pp-log"
            ),
            pipeline_name = f"{web_identity_repo}-{stage}",
            # role = f"{core.Fn.import_value('CodePipelineRoleARN')}",
            stages = [
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            output = codepipeline.Artifact(artifact_name="sourceout"),
                            repository = codecommit.Repository.from_repository_name(
                                self,
                                "WebIdentityStageSource",
                                repository_name = f"{core.Fn.import_value('WebIdentityCodeCommitName')}",
                            ),
                            branch = f"{branch}",
                            action_name = "Source"
                        )
                    ],
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            input = codepipeline.Artifact(artifact_name="sourceout"),
                            project = codebuild.Project.from_project_name(
                                self,
                                "WebIdentityStageBuild",
                                project_name = f"{core.Fn.import_value('WebIdentityCodebuildName')}"
                            ),
                            check_secrets_in_plain_text_env_variables = True,
                            environment_variables = {
                                    "AWS_SECRET_ARN": codebuild.BuildEnvironmentVariable(value = core.Fn.import_value(f"{stage}SecretARN")),
                                    "STAGE": codebuild.BuildEnvironmentVariable(value = stage),
                            },
                            outputs = [
                                codepipeline.Artifact(artifact_name="buildout1")
                            ],
                            action_name = f"{web_identity_repo}-main"
                        )
                    ],
                )
            ]
        )

        self.web_identity_codepipeline_arn = self.web_identity_codepipeline.pipeline_arn

        self.web_identity_cloudwatch_event_rule = events.Rule(
            self,
            "WebIdentityCloudWatchEventRule",
            description = "Amazon CloudWatch Events rule to automatically start your pipeline when a change occurs in the AWS CodeCommit source repository and branch. Deleting this may prevent changes from being detected in that pipeline. Read more: http://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-about-starting.html",
            event_pattern = events.EventPattern(
                source = ["aws.codecommit"],
                detail_type = ["CodeCommit Repository State Change"],
                detail = {
                    "event": ["referenceCreated", "referenceUpdated"],
                    "referenceName": [f"{branch}"],
                    "referenceType": ["branch"]
                },
                resources = [f"{core.Fn.import_value('WebIdentityCodeCommitARN')}"]
            )
        )

        start_pipeline_policy_document={
            "Statement": [
                {
                    "Action": [
                        "codepipeline:StartPipelineExecution"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        f"{self.web_identity_codepipeline_arn}"
                    ]
                }
            ],
            "Version": "2012-10-17"
        }

        custom_start_pipeline_policy_document = iam.PolicyDocument.from_json(start_pipeline_policy_document)

        self.start_pipeline_policy = iam.ManagedPolicy(
            self,
            "StartPipelinePolicy",
            document=custom_start_pipeline_policy_document,
            managed_policy_name=f"start-pipeline-execution-policy-{web_identity_repo}-{stage}", 
            path="/",
        )

        self.start_pipeline_policy_arn =  self.start_pipeline_policy.managed_policy_arn

        self.cwe_role = iam.Role(
            self,
            "CWEWebIdentityRole",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com"),
            role_name=f"cwe-role-{web_identity_repo}-{stage}"
        )

        self.cwe_role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_arn(
            self, 
            "CWEWebIdentityRoleAssignedPolicy", 
            f"{self.start_pipeline_policy_arn}"
            )
        )

        # core.CfnOutput(self, "CodePipelineRoleARN", value=self.code_pipeline_role.role_arn,
        #                export_name="CodePipelineRoleARN")

        self.target = events_targets.CodePipeline(
            pipeline = self.web_identity_codepipeline,
            event_role = self.cwe_role,
        )

        self.target.bind(
            _rule = self.web_identity_cloudwatch_event_rule,
            _id = f"{web_identity_repo}-{stage}"
        )
        
        self.web_identity_cloudwatch_event_rule.add_target(self.target)



