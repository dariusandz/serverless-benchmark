# serverless-benchmark
Prerequisites:
* AWS CLI Tools
* Docker
* Python 3

Note: This tool heavily relies on AWS CLI Tools to configure AWS environment (create user role, create AWS ECR image repository), 
create, deploy, invoke and cleanup lambda functions.

Sources:
* https://github.com/andthearchitect/aws-lambda-java-runtime
* https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
* https://docs.aws.amazon.com/lambda/latest/dg/runtimes-custom.html
* https://docs.aws.amazon.com/lambda/latest/dg/runtimes-walkthrough.html
* https://docs.aws.amazon.com/lambda/latest/dg/runtimes-context.html
* https://docs.aws.amazon.com/lambda/latest/dg/invocation-images.html
* https://docs.aws.amazon.com/lambda/latest/dg/configuration-images.html
* https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
* https://aws.amazon.com/blogs/compute/using-container-image-support-for-aws-lambda-with-aws-sam/