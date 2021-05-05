import re

from Constants import t1_image_tags
from Constants import t1_s1_image_tag, t1_s2_image_tag, t1_s3_image_tag
from Constants import t2_image_tags
from Constants import t2_m1_image_tag
from Constants import t1_logs_dir, t2_logs_dir


def get_logs_root_path(test_num):
    if test_num == "t1":
        return t1_logs_dir
    elif test_num == "t2":
        return t2_logs_dir

    return "undefined-test-num-logs"


def get_test_number_image_tags(test_num):
    if test_num == "t1":
        return t1_image_tags
    if test_num == "t2":
        return t2_image_tags

    return []


def get_fn_tag(fn_name):
    if re.search(re.compile("image-size-s1"), fn_name) is not None:
        return t1_s1_image_tag
    if re.search(re.compile("image-size-s2"), fn_name) is not None:
        return t1_s2_image_tag
    if re.search(re.compile("image-size-s3"), fn_name) is not None:
        return t1_s3_image_tag
    if re.search(re.compile("memory-size-m1"), fn_name) is not None:
        return t2_m1_image_tag

    return "no_tag_found"
