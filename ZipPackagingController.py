from Constants import t3_z1_path, t3_z2_path, t3_z3_path, t3_z3_path_function
from Constants import s3_bucket_name

from util.subprocess_util import run_executable

prepare_zip_exec_path = 'script/zip/prepare-zip.sh'
put_fn_to_s3_exec_path = 'script/aws/function/upload-fn-to-s3.sh'


def main():
    zip_functions()
    put_functions_to_s3()


def zip_functions():
    zip_function(t3_z1_path)
    zip_function(t3_z2_path)
    zip_function(t3_z3_path)


def put_functions_to_s3():
    upload_to_s3(t3_z1_path, "z1")
    upload_to_s3(t3_z2_path, "z2")
    upload_to_s3(t3_z3_path_function, "z3")


def zip_function(path_to_fn):
    run_executable(
        executable_path=prepare_zip_exec_path,
        args=[path_to_fn]
    )


def upload_to_s3(path_to_fn, fn_tag):
    run_executable(
        executable_path=put_fn_to_s3_exec_path,
        args=[path_to_fn, s3_bucket_name, fn_tag]
    )


if __name__ == "__main__":
    main()
