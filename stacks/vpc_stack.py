from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_logs as logs,
    NestedStack
)
import aws_cdk as core
from helper import config

class VPCStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        conf = config.Config(self.node.try_get_context('environment'))
        project_name = conf.get('project_name')
        max_azs = conf.get('max_azs')
        subnet_size = conf.get('subnet_size')
        vpc_cidr = conf.get('vpc_cidr')
        vpc_name = f"{project_name}-VPC-{vpc_cidr}"

        self.vpc_flow_role = iam.Role(
            self, 'FlowLog',
            assumed_by=iam.ServicePrincipal('vpc-flow-logs.amazonaws.com')
        )

        self.vpc = ec2.Vpc(
            self,
            vpc_name,
            enable_dns_hostnames=False,
            enable_dns_support=True,
            ip_addresses=ec2.IpAddresses.cidr(vpc_cidr),
            max_azs=max_azs,
            nat_gateways=max_azs,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Isolation",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=subnet_size
                ),
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=False,
                    cidr_mask=subnet_size
                )
            ]
        )
        
        core.Tags.of(self.vpc).add("Name", f"{project_name}-VPC-{vpc_cidr}")

        # Filter out subnets
        private_subnets_isolated = self.vpc.select_subnets(
            subnet_group_name="Isolation"
        )
        public_subnets = self.vpc.select_subnets(
            subnet_group_name="Public"
        )

        # Naming Subnets
        index = 1
        for subnet in private_subnets_isolated.subnets:
            core.Tags.of(subnet).add(
                "Name", f"{project_name}-Isolation-" + str(index))
            core.CfnOutput(self, f"Isolation-Subnet-{index}", value=private_subnets_isolated.subnet_ids[index-1],
                           export_name=f"IsolationSubnet-{index}")
            index = index + 1

        index = 1
        for subnet in public_subnets.subnets:
            core.Tags.of(subnet).add(
                "Name", f"{project_name}-Public-" + str(index))
            core.CfnOutput(self, f"Public-Subnet-{index}", value=public_subnets.subnet_ids[index-1],
                           export_name=f"PublicSubnet-{index}")
            index = index + 1

        core.CfnOutput(self, "VpcID", value=self.vpc.vpc_id,
                       export_name="VpcID")
        core.CfnOutput(self, "Public-Subnets",
                       value=",".join(str(subnets) for subnets in public_subnets.subnet_ids))
        core.CfnOutput(self, "Private-Subnets",
                       value=",".join(str(subnets) for subnets in private_subnets_isolated.subnet_ids))
