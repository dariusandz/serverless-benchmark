import re

from dotenv import dotenv_values
from Constants import t1_s1_path, t1_s2_path, t1_s3_path
from Constants import t2_m1_path
from util.subprocess_util import run_executable
from util.logging_util import init_logging, log

env_config = dotenv_values()

AWS_DOCKER_REPO = env_config['AWS_ECR_REPOSITORY']

login_aws_docker_exec_path = 'script/docker/docker-aws-login.sh'
build_docker_image_exec_path = './script/docker/gradle-build-docker.sh'
push_docker_image_exec_path = './script/docker/docker-push.sh'

init_logging()


def main():
    aws_docker_login()
    prepare_docker_images()


def aws_docker_login():
    log("Logging in to Docker with AWS credentials")
    aws_region = env_config['AWS_REGION']
    aws_ecr_uri = env_config['AWS_ECR_URI']
    login_response = run_executable(executable_path=login_aws_docker_exec_path, args=[aws_region, aws_ecr_uri])
    log(login_response)


def prepare_docker_images():
    log("Building testable docker images")
    build_and_push_docker_image(t1_s1_path)
    build_and_push_docker_image(t1_s2_path)
    build_and_push_docker_image(t1_s3_path)
    build_and_push_docker_image(t2_m1_path)


def build_and_push_docker_image(path):
    log("Building docker image with path to Dockerfile: {}. This may take some time".format(path))
    docker_build_response = run_executable(executable_path=build_docker_image_exec_path, args=[path, AWS_DOCKER_REPO])
    docker_image_tag = parse_image_tag(docker_build_response)

    docker_push_response = push_to_docker(docker_image_tag)
    log(docker_push_response)


def push_to_docker(image_tag):
    log("Pushing {} to AWS ECR registry".format(image_tag))
    return run_executable(executable_path=push_docker_image_exec_path, args=[image_tag])


def parse_image_tag(docker_response=""):
    log("Parsing built image tag. This may take some time")
    image_tag_regex = re.compile("Successfully tagged \d{12}.\w{3}.\w{3}.\w{2}-\w*-\d.amazonaws.com\/.*")
    try:
        if tag_response := re.search(image_tag_regex, docker_response):
            image_tag = tag_response.group().split(" ").pop()
            log("Built docker image tag is {}".format(image_tag))
            return image_tag
    except TypeError:
        log("Could not parse built docker image tag. Will not be able to push to registry")


if __name__ == "__main__":
    main()
