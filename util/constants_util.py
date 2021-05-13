import re

from Constants import t1_image_tags
from Constants import t1_s1_image_tag, t1_s2_image_tag, t1_s3_image_tag
from Constants import t2_image_tags
from Constants import t2_m1_image_tag
from Constants import t3_z1_tag, t3_z2_tag, t3_z3_tag, t3_function_name
from Constants import t3_z1_path, t3_z2_path, t3_z3_path_function
from Constants import t1_logs_dir, t2_logs_dir, t3_logs_dir


def get_logs_root_path(test_num):
    if test_num == "t1":
        return t1_logs_dir
    elif test_num == "t2":
        return t2_logs_dir
    elif test_num == "t3":
        return t3_logs_dir

    return "undefined-test-num-logs"


def get_test_number_image_tags(test_num):
    if test_num == "t1":
        return t1_image_tags
    if test_num == "t2":
        return t2_image_tags

    return []


# Tag for images | fn-name + tag for zips
def get_fn_package_identifier(fn_name):
    if re.search(re.compile("image-size-s1"), fn_name) is not None:
        return t1_s1_image_tag
    if re.search(re.compile("image-size-s2"), fn_name) is not None:
        return t1_s2_image_tag
    if re.search(re.compile("image-size-s3"), fn_name) is not None:
        return t1_s3_image_tag
    if re.search(re.compile("memory-size-m1"), fn_name) is not None:
        return t2_m1_image_tag
    if re.search(re.compile("zip-package-z1"), fn_name) is not None:
        return t3_z1_tag
    if re.search(re.compile("zip-package-z2"), fn_name) is not None:
        return t3_z2_tag
    if re.search(re.compile("zip-package-z3"), fn_name) is not None:
        return t3_z3_tag

    return "no_tag_found"


def get_zip_fn_path(zip_fn_tag):
    if zip_fn_tag == "z1":
        return t3_z1_path
    if zip_fn_tag == "z2":
        return t3_z2_path
    if zip_fn_tag == "z3":
        return t3_z3_path_function

    return "undefined-function-path"
