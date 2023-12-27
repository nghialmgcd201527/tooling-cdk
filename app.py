#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.vpc_stack import VPCStack
from stacks.iam.iam_group_stack import IamGroupStack
from stacks.iam.iam_policy.iam_policy_devops_stack import IamPolicyDevopsStack
from stacks.iam.iam_policy.iam_policy_maintainers_stack import IamPolicyMaintainersStack
from stacks.iam.iam_policy.iam_policy_developers_stack import IamPolicyDevelopersStack
from stacks.iam.iam_role_codebuild.iam_role_codebuild_fe_stack import IamRoleCodebuildFeStack
from stacks.iam.iam_role_codebuild.iam_role_codebuild_be_stack import IamRoleCodebuildBeStack
from stacks.secret_manager_stack import SecretManagerStack
from stacks.codecommit_fe.web_identity_stack import WebIdentityCodecommitStack
from stacks.codecommit_fe.web_admin_stack import WebAdminCodecommitStack
from stacks.codecommit_fe.web_component_stack import WebComponentCodecommitStack
from stacks.codecommit_be.file_svc import FileServiceCodecommitStack
from stacks.codebuild_fe.web_identity_stack import WebIdentityCodebuildStack
from stacks.codebuild_be.file_service_stack import FileServiceCodebuildStack
from stacks.codepipeline_fe.web_identity_stack import WebIdentityCodePipelineStack
from stacks.iam.iam_role_codepipeline_stack import IamRoleCodePipelineStack

import cdk_nag
from helper import config
from aws_cdk import (
    Aspects,
)

app = cdk.App()
conf_app = config.Config(app.node.try_get_context('environment'))
vpc_stack = VPCStack(app, 
                    "vpc-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_group_stack = IamGroupStack(app, 
                    "iam-group-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_policy_devops_stack = IamPolicyDevopsStack(app,
                    "iam-policy-devops-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_policy_maintainers_stack = IamPolicyMaintainersStack(app,
                    "iam-policy-maintainers-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_policy_developers_stack = IamPolicyDevelopersStack(app,
                    "iam-policy-developers-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_role_codebuild_fe_stack = IamRoleCodebuildFeStack(app,
                    "iam-role-codebuild-fe-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_role_codebuild_be_stack = IamRoleCodebuildBeStack(app,
                    "iam-role-codebuild-be-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

iam_role_codepipeline_stack = IamRoleCodePipelineStack(app,
                    "iam-role-codepipeline-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

secret_manager_stack = SecretManagerStack(app,
                    "secret-manager-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

web_identity_codecommit_stack = WebIdentityCodecommitStack(app,
                    "web-identity-codecommit-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

web_admin_codecommit_stack = WebAdminCodecommitStack(app,
                    "web-admin-codecommit-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

web_component_codecommit_stack = WebComponentCodecommitStack(app,
                    "web-component-codecommit-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

file_service_codecommit_stack = FileServiceCodecommitStack(app,
                    "file-service-codecommit-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

web_identity_codebuild_stack = WebIdentityCodebuildStack(app,
                    "web-identity-codebuild-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

file_service_codebuild_stack = FileServiceCodebuildStack(app,
                    "file-service-codebuild-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

web_identity_codepipeline_stack = WebIdentityCodePipelineStack(app,
                    "web-identity-codepipeline-stack",
                    env=cdk.Environment(account=conf_app.get('account_id'),
                    region=conf_app.get('region')))

Aspects.of(app).add(cdk_nag.AwsSolutionsChecks())
app.synth()
