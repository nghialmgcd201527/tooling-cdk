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

class IamGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        conf = config.Config(self.node.try_get_context('environment'))
        account_id = conf.get('account_id')
        
        # with open('./policy/codecommit-policies-devops.json') as codecommit_policies_devops_json:
        #     codecommit_policies_devops = json.load(codecommit_policies_devops_json)
        # for item in codecommit_policies_devops['Statement']:
        #     item['Resource'] = item['Resource'].replace('$ACCOUNT_ID', account_id)
        # with open('./policy/new-codecommit-policies-devops.json', 'w') as codecommit_policies_devops_json:
        #     json.dump(codecommit_policies_devops, codecommit_policies_devops_json)

        # with open('./policy/codecommit-policies-maintainers.json') as codecommit_policies_maintainers_json:
        #     codecommit_policies_maintainers = json.load(codecommit_policies_maintainers_json)
        # for item in codecommit_policies_maintainers['Statement']:
        #     item['Resource'] = item['Resource'].replace('$ACCOUNT_ID', account_id)
        # with open('./policy/new-codecommit-policies-maintainers.json', 'w') as codecommit_policies_maintainers_json:
        #     json.dump(codecommit_policies_maintainers, codecommit_policies_maintainers_json)

        # self.DevOps_policy = iam.CfnManagedPolicy(
        #     self,
        #     "DevOps Policy",
        #     managed_policy_name="CodeCommit-Policies-DevOps", 
        #     path="/",
        #     policy_document=json.load('./policy/new-codecommit-policies-devops.json'),
        # )
        # self.Maintainers_policy = iam.CfnManagedPolicy(
        #     self,
        #     "Maintainers Policy",
        #     managed_policy_name="CodeCommit-Policies-Maintainers",
        #     path="/",
        #     policy_document=json.load('./policy/new-codecommit-policies-maintainers.json'),
        # )

        self.DevOps_group = iam.CfnGroup(
            self, 
            "DevOps",
            group_name="DevOps",
            path="/",
        )

        self.Maintainers_group = iam.CfnGroup(
            self, 
            "Maintainers",
            group_name="Maintainers",
            path="/",
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess",
                "arn:aws:iam::aws:policy/AWSCodePipeline_FullAccess"    
            ]
        )

        self.Developers_group = iam.CfnGroup(
            self, 
            "Developers",
            group_name="Developers",
            path="/",
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/IAMSelfManageServiceSpecificCredentials",
                "arn:aws:iam::aws:policy/IAMUserSSHKeys",
                "arn:aws:iam::aws:policy/AWSCodeArtifactReadOnlyAccess"    
            ]
        )

        core.CfnOutput(self, "DevOpsGroup", value=self.DevOps_group.group_name,
                       export_name="DevOps")
        core.CfnOutput(self, "MaintainersGroup", value=self.Maintainers_group.group_name,
                       export_name="Maintainers")
        core.CfnOutput(self, "DevelopersGroup", value=self.Developers_group.group_name,
                       export_name="Developers")

