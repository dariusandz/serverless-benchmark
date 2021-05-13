from Constants import t3_z1_path, t3_z2_path, t3_z3_path, t3_z3_path_function, t3_z3_path_runtime
from Constants import s3_bucket_name, t3_z3_runtime_layer_name

from util.subprocess_util import run_executable
from util.logging_util import log

prepare_zip_exec_path = 'script/zip/prepare-zip.sh'
put_fn_to_s3_exec_path = 'script/aws/function/upload-fn-to-s3.sh'
create_runtime_layer_exec_path = 'script/aws/zip/create-lambda-layer.sh'


def main():
    zip_functions()
    put_functions_to_s3()
    create_runtime_layer()


def zip_functions():
    zip_function(t3_z1_path)
    zip_function(t3_z2_path)
    zip_function(t3_z3_path)


def put_functions_to_s3():
    upload_to_s3(t3_z1_path, "z1")
    upload_to_s3(t3_z2_path, "z2")
    upload_to_s3(t3_z3_path_function, "z3")


def zip_function(path_to_fn):
    log("Zipping function with path {}".format(path_to_fn))
    run_executable(
        executable_path=prepare_zip_exec_path,
        args=[path_to_fn]
    )


def upload_to_s3(path_to_fn, fn_tag):
    log("Uploading function {}-{} zip to s3".format(path_to_fn, fn_tag))
    run_executable(
        executable_path=put_fn_to_s3_exec_path,
        args=[path_to_fn, s3_bucket_name, fn_tag]
    )


def create_runtime_layer():
    log("Creating runtime layer {} from {}".format(t3_z3_runtime_layer_name, t3_z3_path_runtime))
    run_executable(
        executable_path=create_runtime_layer_exec_path,
        args=[t3_z3_runtime_layer_name, t3_z3_path_runtime]
    )


if __name__ == "__main__":
    main()
