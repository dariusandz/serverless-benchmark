import argparse
import os
import re
import pandas
import matplotlib.pyplot as plt

from dotenv import dotenv_values
from logging import ERROR

from Constants import logs_dir_path, results_dir_path, t2_function_memory_sizes

from os.path import isfile, join
from TranslationService import translate, genitive_case
from util.constants_util import get_logs_root_path, get_fn_tag
from util.file_util import read_file, read_csv_to_dataframe, write_to_csv
from util.subprocess_util import run_executable
from util.logging_util import log, init_logging

env_config = dotenv_values()

REPOSITORY_NAME = env_config["AWS_ECR_REPOSITORY_NAME"]

describe_image_exec_path = './script/aws/environment/describe-image.sh'

results_header = ["image_size_mb", "memory_size_mb", "init_duration_ms"]

init_logging()


parser = argparse.ArgumentParser(description="Results Parser")
parser.add_argument("-t", "--test", type=str)


def main():
    args = parser.parse_args()
    test_num = args.test

    parse_logs(test_num)


def parse_logs(test_num):
    log(f'Parsing logs for test: {test_num}')
    test_logs_path = get_logs_root_path(test_num)
    logs_dir = f'{logs_dir_path}/{test_logs_path}/'

    for log_dir in os.listdir(logs_dir):
        fn_name = log_dir
        fn_logs_dir = logs_dir + fn_name

        image_size_mb = get_fn_image_size(fn_name)
        csv_results = []
        for log_file in os.listdir(fn_logs_dir):
            log(f'Parsing logs file {log_file}')
            fn_log = read_file(fn_logs_dir + '/' + log_file)

            csv_results.append([image_size_mb, get_memory_size(fn_log), get_init_duration(fn_log)])

        full_path = results_dir_path + test_logs_path + fn_name + '.csv'
        write_to_csv(csv_results, results_header, full_path)

    write_average_init_duration(test_num, results_dir_path + test_logs_path)


def get_memory_size(fn_log):
    memory_size_regex = re.compile("Memory Size: \d*")
    try:
        if memory_size := re.search(memory_size_regex, fn_log):
            return int(memory_size.group().replace("Memory Size: ", "").strip())
    except TypeError:
        log("Could not parse Memory Size from lambda invocation log", ERROR)


def get_init_duration(fn_log):
    billed_duration_regex = re.compile("Init Duration: \d*.\d*")
    try:
        if billed_duration := re.search(billed_duration_regex, fn_log):
            return float(billed_duration.group().replace("Init Duration: ", "").strip())
    except TypeError:
        log("Could not parse Init Duration from lambda invocation log", ERROR)

    return 0


def get_fn_image_size(fn_name):
    fn_tag = get_fn_tag(fn_name)
    image_details = run_executable(
        executable_path=describe_image_exec_path,
        args=[REPOSITORY_NAME, fn_tag]
    )

    image_byte_size_regex = re.compile("\"imageSizeInBytes\": \\d*")
    try:
        if image_byte_size := re.search(image_byte_size_regex, image_details):
            image_bytes = int(image_byte_size.group().replace("\"imageSizeInBytes\": ", ""))
            return round(image_bytes / 1000 / 1000, 2)
    except TypeError:
        log("Could not get function image size. This might be because provided image name is wrong", ERROR)

    return 0


def write_average_init_duration(test_num, results_path):
    if test_num == 't1':
        get_average_by('image_size_mb', test_num, results_path)
    if test_num == 't2':
        get_average_by('memory_size_mb', test_num, results_path)


def get_average_by(by, test_num, results_path):
    result_files = get_results_path(results_path)
    data_frames = []
    for file in result_files:
        data_frames.append(read_csv_to_dataframe(results_path + file))
    df = pandas.concat(data_frames).round(2)
    df_grouped = df.groupby(by).mean()
    plot(df_grouped["init_duration_ms"], test_num, by)


def plot(df, test_num, xlabel):
    plot_kind = get_plot_kind(test_num)
    title = translate("chart_title", genitive_case(xlabel))

    if test_num == "t1":
        df.plot(
            x=xlabel,
            xlabel=translate(xlabel),
            y=["init_duration_ms"],
            ylabel=translate('init_duration_ms'),
            title=title,
            kind=plot_kind,
        )
    else:
        df.plot(
            x=xlabel,
            xlabel=translate(xlabel),
            xticks=df.keys(),
            y=["init_duration_ms"],
            ylabel=translate('init_duration_ms'),
            title=title,
            kind=plot_kind,
            grid=True,
        )

    plt.show()


def get_plot_kind(test_num):
    if test_num == 't2':
        return 'line'
    else:
        return 'bar'


def get_results_path(results_path):
    return [f for f in os.listdir(results_path) if isfile(join(results_path, f))]


if __name__ == "__main__":
    main()
