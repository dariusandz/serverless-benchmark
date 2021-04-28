import re

from util.subprocess_util import run_executable
from util.logging_util import init_logging, log
from util.sleep_util import sleep
from util.file_util import write_to_file

create_ecr_repository_exec_path = 'script/aws/environment/create-aws-ecr-repository.sh'
create_role_exec_path = 'script/aws/environment/create-aws-lambda-role.sh'
assign_role_permissions_exec_path = 'script/aws/environment/assign-aws-lambda-role-permissions.sh'

init_logging()


def main():
    image_repository = create_aws_ecr_image_repository()
    role_arn = create_aws_role()
    assign_aws_role_lambda_permissions()
    write_to_dotenv(
        [
            "AWS_REGION={}".format(extract_aws_region(image_repository)),
            "AWS_ECR_URI={}".format(extract_aws_ecr_uri(image_repository)),
            "AWS_ECR_REPOSITORY_NAME={}".format(extract_aws_ecr_repository_name(image_repository)),
            "AWS_ECR_REPOSITORY={}".format(image_repository),
            "AWS_ROLE_ARN={}".format(role_arn)
        ]
    )


def create_aws_ecr_image_repository():
    log("Creating AWS ecr image repository")
    repository_uri_regex = re.compile("\d{12}.\w{3}.\w{3}.\w{2}-\w*-\d.amazonaws.com/[^\"]*")
    result = run_executable(executable_path=create_ecr_repository_exec_path)
    if repository_uri := re.search(repository_uri_regex, result):
        repository = repository_uri.group()
        log("AWS ecr image created successfully under the name {}".format(repository))
        return repository


def create_aws_role():
    log("Creating AWS IAM role")
    arn_regex = re.compile("arn:aws[a-zA-Z-]*?:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+")
    result = run_executable(executable_path=create_role_exec_path)
    if arn_role := re.search(arn_regex, result):
        role_arn = arn_role.group()
        log("AWS IAM role created successfully under the ARN {}".format(role_arn))
        sleep(30)  # AWS takes some time to process our request
        return arn_role.group()


def assign_aws_role_lambda_permissions():
    log("Assigning AWS IAM role permissions")
    run_executable(executable_path=assign_role_permissions_exec_path)


def extract_aws_region(image_registry_uri=""):
    log("Parsing AWS region")
    region_regex = re.compile("\w{2}-\w*-[^.]")
    try:
        if aws_region := re.search(region_regex, image_registry_uri):
            region = aws_region.group()
            log("Defined AWS region is {}".format(region))
            return region
    except TypeError:
        log("Could not parse AWS region")


def extract_aws_ecr_uri(image_registry_uri=""):
    log("Parsing AWS ecr uri")
    ecr_regex = re.compile("\d{12}.\w{3}.\w{3}.\w{2}-\w*-\d.amazonaws.com")
    try:
        if ecr_uri := re.search(ecr_regex, image_registry_uri):
            ecr = ecr_uri.group()
            log("Defined AWS ecr uri is {}".format(ecr))
            return ecr
    except TypeError:
        log("Could not parse AWS ecr uri")


def extract_aws_ecr_repository_name(image_registry_uri=""):
    log("Parsing AWS ecr repository name")
    repo_name_regex = re.compile("/.*")
    try:
        if repo_name := re.search(repo_name_regex, image_registry_uri):
            name = repo_name.group().replace("/", "")
            log("Defined AWS repository name is {}".format(name))
            return name
    except TypeError:
        log("Could not parse AWS repository name")


def write_to_dotenv(env_variables):
    write_to_file(env_variables, "./.env")


if __name__ == "__main__":
    main()
