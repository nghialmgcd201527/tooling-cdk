import aws_cdk as core
import aws_cdk.assertions as assertions

from dh_tooling_cdk_template.dh_tooling_cdk_template_stack import DhToolingCdkTemplateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in dh_tooling_cdk_template/dh_tooling_cdk_template_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DhToolingCdkTemplateStack(app, "dh-tooling-cdk-template")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
