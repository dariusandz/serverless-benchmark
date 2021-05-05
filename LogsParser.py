import re

from datetime import datetime
from logging import DEBUG, ERROR

from Constants import logs_dir_path

from util.constants_util import get_logs_root_path
from util.file_util import write_to_file
from util.base64_util import decode_base64
from util.logging_util import log


def write_response_logs(fn_name, invocation_response, test_num):
    log_str = parse_response_logs(fn_name, invocation_response)
    if not is_cold_started(log_str):
        return

    test_num_logs_path = get_logs_root_path(test_num)
    uuid_regex = re.compile("[0-9a-f]{8}\\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\\b[0-9a-f]{12}")
    try:
        if uuid := re.search(uuid_regex, fn_name):
            fn_id = uuid.group()
            now = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            log_dir = f'{logs_dir_path}/{test_num_logs_path}/{fn_name.replace(fn_id, "")}/{now}-{fn_id}'
            write_to_file(log_str, log_dir)
    except TypeError:
        log("Could not parse request id from invocation logs", ERROR)


def parse_response_logs(fn_name, invocation_response):
    log("Parsing function {} invocation response logs".format(fn_name))
    log_result_regex = re.compile("\"LogResult\": [^,]*")
    base64_log = ""
    try:
        if log_result := re.search(log_result_regex, invocation_response):
            base64_log = log_result.group().replace("\"LogResult\": ", "").replace("\"", "")
    except TypeError:
        log("Could not parse invocation log")
        return base64_log

    return decode_base64(base64_log)


def is_cold_started(log_str):
    is_cold_start_log_regex = re.compile("Invoked a cold start function")
    try:
        if re.search(is_cold_start_log_regex, log_str):
            return True
        else:
            log("Function was not started cold. Skipping writing log", DEBUG)
            return False
    except TypeError:
        return False
