import argparse
import uuid
import timeit

from dotenv import dotenv_values
from subprocess import CalledProcessError
from logging import ERROR, DEBUG

from Constants import s3_bucket_name
from Constants import custom_runtime_tags, providable_runtime_tags, attachable_runtime_layer_tags
from Constants import t4_memory_size, t1_memory_size, t1_s1_image_tag, t1_s2_image_tag, t1_s3_image_tag, t1_function_name
from Constants import t2_function_memory_sizes_1, t2_m1_image_tag, t2_function_name
from Constants import t3_memory_size, t3_z1_tag, t3_z2_tag, t3_z3_tag, t3_z3_path_runtime, t3_function_name, t3_z3_runtime_layer_name
from Constants import t4_p1_image_tag, t4_p2_image_tag, t4_p3_image_tag, t4_function_name

from LogsParser import write_response_logs

from util.sleep_util import sleep
from util.subprocess_util import run_executable
from util.logging_util import init_logging, log
from util.constants_util import get_zip_fn_path

create_lambda_function_from_image_exec_path = 'script/aws/function/create-lambda-function-package-image.sh'
create_lambda_function_from_zip_exec_path = 'script/aws/function/create-lambda-function-package-zip.sh'
attach_lambda_layer_exec_path = 'script/aws/function/attach-lambda-layer.sh'
config_lambda_function_exec_path = 'script/aws/function/update-lambda-configuration.sh'
invoke_lambda_function_exec_path = 'script/aws/function/invoke-lambda-function.sh'
delete_lambda_function_exec_path = 'script/aws/function/delete-lambda-function.sh'

env_config = dotenv_values()

AWS_ECR_REPOSITORY_URI = env_config["AWS_ECR_REPOSITORY"]
AWS_ROLE_ARN = env_config["AWS_ROLE_ARN"]
AWS_ROLE_ARN_ID = env_config["AWS_ROLE_ARN_ID"]

init_logging()

parser = argparse.ArgumentParser(description="Test Controller")
parser.add_argument("-t", "--test", type=str)
parser.add_argument("-c", "--count", type=str)

RETRY_COUNT = 10
RETRY_COOLDOWN = 3

time_for_response = lambda x: "Wait for response duration: {} ms".format(x)
layer_attachment = lambda x: "Layer attachment duration: {} ms".format(x)


def main():
    args = parser.parse_args()
    test_num = args.test
    num_invocations = int(args.count)

    if test_num == "t1":
        repeat_fun(num_invocations, test_jar_size)

    if test_num == "t2":
        repeat_fun(num_invocations, test_mem_size)

    if test_num == "t3":
        repeat_fun(num_invocations, test_zip_packaging)

    if test_num == "t4":
        repeat_fun(num_invocations, test_minimal_docker_image)


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

        run_docker_image_test_steps(
            "t1", function_name, t1_memory_size, image_tag, aws_image_uri
        )


def test_mem_size():
    log("Running allocated memory size tests")
    for memory_size in t2_function_memory_sizes_1:
        aws_image_uri = build_image_uri(t2_m1_image_tag)
        function_name = build_function_name(t2_function_name, t2_m1_image_tag) + str(uuid.uuid4())

        run_docker_image_test_steps(
            "t2", function_name, memory_size, t2_m1_image_tag, aws_image_uri
        )


def test_zip_packaging():
    log("Running zip package tests")
    t3_tags = [t3_z1_tag, t3_z2_tag, t3_z3_tag]
    for zip_tag in t3_tags:
        function_name = build_function_name(t3_function_name, zip_tag + str(uuid.uuid4()))

        run_zip_package_test_steps(
            "t3", function_name, t3_memory_size, get_zip_fn_path(zip_tag), zip_tag
        )


def test_minimal_docker_image():
    log("Running minimal docker image size tests")
    t4_image_tags = [t4_p1_image_tag, t4_p2_image_tag, t4_p3_image_tag]
    for image_tag in t4_image_tags:
        aws_image_uri = build_image_uri(image_tag)
        function_name = build_function_name(t4_function_name, image_tag) + str(uuid.uuid4())

        run_docker_image_test_steps(
            "t4", function_name, t4_memory_size, image_tag, aws_image_uri
        )


def build_image_uri(tag):
    return AWS_ECR_REPOSITORY_URI + ':' + tag


def build_function_name(test_num_function_name, tag):
    return test_num_function_name + '-' + tag


def run_docker_image_test_steps(test_num, fn_name, mem_size, image_tag, aws_image_uri):
    deploy_docker_image_function(fn_name, mem_size, aws_image_uri, AWS_ROLE_ARN)
    config_duration = configure_function_runtime(fn_name, image_tag)
    invoke_function(fn_name, test_num, config_duration)
    delete_function(fn_name)


def run_zip_package_test_steps(test_num, fn_name, fn_memory_size, fn_path, fn_tag):
    runtime = "provided" if fn_tag in providable_runtime_tags else "java11"

    deploy_zip_package_function(fn_name, fn_memory_size, fn_path, AWS_ROLE_ARN, fn_tag, runtime)
    layer_config_duration = configure_function_layer(fn_name, fn_tag, AWS_ROLE_ARN_ID)
    invoke_function(fn_name, test_num, layer_config_duration)
    delete_function(fn_name)


def deploy_zip_package_function(fn_name, fn_memory_size, fn_path, role_arn, fn_tag, runtime="java11"):
    log("Deploying zipped function {} with size {} with runtime {}".format(fn_path, fn_memory_size, runtime))
    try:
        deploy_response = run_executable(
            executable_path=create_lambda_function_from_zip_exec_path,
            args=[fn_name, str(fn_memory_size), role_arn, runtime, s3_bucket_name, fn_tag]
        )
        log("Deployment request sent")
        log("Deployment result: \n{}".format(deploy_response), DEBUG)
    except CalledProcessError:
        log("Something went wrong. This might be because your function is already deployed", ERROR)


def deploy_docker_image_function(fn_name, fn_memory_size, image_uri, role_arn):
    log("Deploying docker image function {} with size {} with image {} for role_arn {}".format(fn_name, fn_memory_size, image_uri, role_arn))
    try:
        deploy_response = run_executable(
            executable_path=create_lambda_function_from_image_exec_path,
            args=[fn_name, str(fn_memory_size), image_uri, role_arn]
        )
        log("Deployment request sent")
        log("Deployment result: \n{}".format(deploy_response), DEBUG)
    except CalledProcessError:
        log("Something went wrong. This might be because your function is already deployed", ERROR)


def configure_function_layer(fn_name, fn_tag, role_arn_id, layer_name=t3_z3_runtime_layer_name, retries=0):
    if fn_tag in attachable_runtime_layer_tags:
        try:
            log("Attaching function {} with runtime layer".format(fn_name))
            configure_layer_start = timeit.default_timer()
            config_response = run_executable(
                executable_path=attach_lambda_layer_exec_path,
                args=[fn_name, role_arn_id, layer_name]
            )
            configure_layer_duration_ms = round((timeit.default_timer() - configure_layer_start) * 1000, 2)
            log("Configured successfully")
            log("Resulting config: \n{}".format(config_response), DEBUG)
            return configure_layer_duration_ms
        except CalledProcessError:
            log("Something went wrong. This might be because your function deployment is not yet processed by AWS", ERROR)
            if retries < RETRY_COUNT:
                log("Retrying function configuration")
                sleep(RETRY_COOLDOWN)
                configure_function_runtime(fn_name, fn_tag, retries + 1)
        return 0


def configure_function_runtime(fn_name, fn_tag, retries=0):
    if fn_tag in custom_runtime_tags:
        try:
            log("Configuring function {} with custom runtime".format(fn_name))
            configure_layer_start = timeit.default_timer()
            config_response = run_executable(
                executable_path=config_lambda_function_exec_path,
                args=[fn_name]
            )
            configure_layer_duration_ms = round((timeit.default_timer() - configure_layer_start) * 1000, 2)
            log("Configured successfully")
            log("Resulting config: \n{}".format(config_response), DEBUG)
            return configure_layer_duration_ms
        except CalledProcessError:
            log("Something went wrong. This might be because your function deployment is not yet processed by AWS", ERROR)
            if retries < RETRY_COUNT:
                log("Retrying function configuration")
                sleep(RETRY_COOLDOWN)
                configure_function_runtime(fn_name, fn_tag, retries + 1)
        return 0


def invoke_function(fn_name, test_num, config_time, retries=0):
    log("Invoking function {}".format(fn_name))
    if config_time is None:
        config_time = 0
    try:
        invocation_start = timeit.default_timer()
        invocation_response = run_executable(
            executable_path=invoke_lambda_function_exec_path,
            args=[fn_name]
        )
        time_for_response_ms = round((timeit.default_timer() - invocation_start) * 1000, 2)
        write_response_logs(
            fn_name,
            invocation_response,
            test_num,
            [time_for_response(time_for_response_ms), layer_attachment(config_time)]
        )
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
