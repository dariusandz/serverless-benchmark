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
    if fn_name == "image-size-s1":
        return t1_s1_image_tag
    if fn_name == "image-size-s2":
        return t1_s2_image_tag
    if fn_name == "image-size-s3":
        return t1_s3_image_tag
    if fn_name == "memory-size-m1":
        return t2_m1_image_tag

    return "no_tag_found"
