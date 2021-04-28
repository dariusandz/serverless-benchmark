import argparse
import uuid

from dotenv import dotenv_values
from subprocess import CalledProcessError
from logging import ERROR, DEBUG

from Constants import custom_runtime_tags
from Constants import t1_memory_size, t1_s1_image_tag, t1_s2_image_tag, t1_s3_image_tag, t1_function_name
from Constants import t2_function_memory_sizes, t2_m1_image_tag, t2_function_name

from LogsParser import write_response_logs

from util.sleep_util import sleep
from util.subprocess_util import run_executable
from util.logging_util import init_logging, log

create_lambda_function_exec_path = 'script/aws/function/create-lambda-function.sh'
config_lambda_function_exec_path = 'script/aws/function/update-lambda-configuration.sh'
invoke_lambda_function_exec_path = 'script/aws/function/invoke-lambda-function.sh'
delete_lambda_function_exec_path = 'script/aws/function/delete-lambda-function.sh'

env_config = dotenv_values()

AWS_ECR_REPOSITORY_URI = env_config["AWS_ECR_REPOSITORY"]
AWS_ROLE_ARN = env_config["AWS_ROLE_ARN"]

init_logging()

parser = argparse.ArgumentParser(description="Test Controller")
parser.add_argument("-t", "--test", type=str)
parser.add_argument("-c", "--count", type=str)

RETRY_COUNT = 10
RETRY_COOLDOWN = 3


def main():
    args = parser.parse_args()
    test_num = args.test
    num_invocations = int(args.count)

    if test_num == "t1":
        repeat_fun(num_invocations, test_jar_size)

    if test_num == "t2":
        repeat_fun(num_invocations, test_mem_size)


def repeat_fun(times, f):
    for i in range(times):
        log("Test iteration: {}".format(i))
        f()


def test_jar_size():
    log("Running container image size tests")
    t1_image_tags = [t1_s1_image_tag, t1_s2_image_tag, t1_s3_image_tag]
    for image_tag in t1_image_tags:
        aws_image_uri = build_image_uri(image_tag)
        function_name = build_function_name(t1_function_name, image_tag) + str(uuid.uuid4())

        run_test_steps(
            "t1", function_name, t1_memory_size, image_tag, aws_image_uri
        )


def test_mem_size():
    log("Running allocated memory size tests")
    for memory_size in t2_function_memory_sizes:
        aws_image_uri = build_image_uri(t2_m1_image_tag)
        function_name = build_function_name(t2_function_name, t2_m1_image_tag) + str(uuid.uuid4())

        run_test_steps(
            "t2", function_name, memory_size, t2_m1_image_tag, aws_image_uri
        )


def build_image_uri(tag):
    return AWS_ECR_REPOSITORY_URI + ':' + tag


def build_function_name(test_num_function_name, tag):
    return test_num_function_name + '-' + tag


def run_test_steps(test_num, fn_name, mem_size, image_tag, aws_image_uri):
    deploy_function(fn_name, mem_size, aws_image_uri, AWS_ROLE_ARN)
    configure_function(fn_name, image_tag)
    invoke_function(fn_name, test_num)
    delete_function(fn_name)


def deploy_function(fn_name, fn_memory_size, image_uri, role_arn):
    log("Deploying function {} with size {} with image {} for role_arn {}".format(fn_name, fn_memory_size, image_uri, role_arn))
    try:
        deploy_response = run_executable(
            executable_path=create_lambda_function_exec_path,
            args=[fn_name, str(fn_memory_size), image_uri, role_arn]
        )
        log("Deployment request sent")
        log("Deployment result: \n{}".format(deploy_response), DEBUG)
        log("Sleeping for some time for AWS to process request.", DEBUG)
    except CalledProcessError:
        log("Something went wrong. This might be because your function is already deployed", ERROR)


def configure_function(fn_name, fn_tag, retries=0):
    if fn_tag in custom_runtime_tags:
        try:
            log("Configuring function {} with custom runtime".format(fn_name))
            config_response = run_executable(
                executable_path=config_lambda_function_exec_path,
                args=[fn_name]
            )
            log("Configured successfully")
            log("Resulting config: \n{}".format(config_response), DEBUG)
        except CalledProcessError:
            log("Something went wrong. This might be because your function deployment is not yet processed by AWS", ERROR)
            if retries < RETRY_COUNT:
                log("Retrying function configuration")
                sleep(RETRY_COOLDOWN)
                configure_function(fn_name, fn_tag, retries + 1)


def invoke_function(fn_name, test_num, retries=0):
    log("Invoking function {}".format(fn_name))
    try:
        invocation_response = run_executable(
            executable_path=invoke_lambda_function_exec_path,
            args=[fn_name]
        )
        write_response_logs(fn_name, invocation_response, test_num)
        log("Invoked successfully")
        log("Invocation response: \n{}".format(invocation_response), DEBUG)
    except CalledProcessError:
        log("Something went wrong. This might be because your function deployment is not yet processed by AWS", ERROR)
        if retries < RETRY_COUNT:
            log("Retrying function invocation")
            sleep(RETRY_COOLDOWN)
            invoke_function(fn_name, test_num, retries + 1)


def delete_function(fn_name):
    log("Deleting function {}".format(fn_name))
    try:
        deletion_response = run_executable(
            executable_path=delete_lambda_function_exec_path,
            args=[fn_name]
        )
        log("Deleted successfully")
        log("Deletion response: {}".format(deletion_response), DEBUG)
    except CalledProcessError:
        log("Something went wrong. This might be because your function does not exist", ERROR)


if __name__ == "__main__":
    main()
