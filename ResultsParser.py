import argparse
import os
import re
import pandas
import matplotlib.pyplot as plt

from dotenv import dotenv_values
from logging import ERROR

from Constants import s3_bucket_name
from Constants import logs_dir_path, results_dir_path

from subprocess import CalledProcessError
from os.path import isfile, join
from Constants import mem_per_1vCPU
from TranslationService import translate, genitive_case
from util.constants_util import get_logs_root_path, get_fn_package_identifier
from util.file_util import read_file, read_csv_to_dataframe, write_to_csv
from util.subprocess_util import run_executable
from util.logging_util import log, init_logging

env_config = dotenv_values()

REPOSITORY_NAME = env_config["AWS_ECR_REPOSITORY_NAME"]

describe_image_exec_path = './script/aws/environment/describe-image.sh'
describe_s3_object_exec_path = './script/aws/environment/describe-s3-object.sh'

results_header = ["function_code_package_size_mb", "memory_size_mb", "init_duration_ms", "artificial_init_duration", "duration_ms", "billed_duration_ms", "wait_for_response_durations_ms", "layer_configuration_duration_ms", "available_threads"]

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

        fn_package_size = get_fn_package_size_mb(fn_name)
        csv_results = []
        for log_file in os.listdir(fn_logs_dir):
            log(f'Parsing logs file {log_file} in dir {fn_logs_dir}')
            fn_log = read_file(fn_logs_dir + '/' + log_file)

            csv_results.append([
                fn_package_size,
                get_memory_size(fn_log),
                get_init_duration(fn_log),
                get_artificial_init_duration(fn_log),
                get_duration(fn_log),
                get_billed_duration(fn_log),
                get_wait_for_response_duration(fn_log),
                get_layer_configuration_duration(fn_log),
                get_available_threads(fn_log)
            ])

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


def get_duration(fn_log):
    init_duration_regex = re.compile("Duration: \d*.\d*")
    try:
        if init_duration := re.search(init_duration_regex, fn_log):
            return float(init_duration.group().replace("Duration: ", "").strip())
    except TypeError:
        log("Could not parse Duration from lambda invocation log", ERROR)

    return 0


def get_init_duration(fn_log):
    init_duration_regex = re.compile("Init Duration: \d*.\d*")
    try:
        if init_duration := re.search(init_duration_regex, fn_log):
            return float(init_duration.group().replace("Init Duration: ", "").strip())
    except TypeError:
        log("Could not parse Init Duration from lambda invocation log", ERROR)

    return 0


def get_billed_duration(fn_log):
    billed_duration_regex = re.compile("Billed Duration: \d*.\d*")
    try:
        if billed_duration := re.search(billed_duration_regex, fn_log):
            return float(billed_duration.group().replace("Billed Duration: ", "").strip())
    except TypeError:
        log("Could not parse Billed Duration from lambda invocation log", ERROR)

    return 0


def get_artificial_init_duration(fn_log):
    billed_duration_regex = re.compile("Artificial initialization duration took: \d*.\d*")
    try:
        if billed_duration := re.search(billed_duration_regex, fn_log):
            return float(billed_duration.group().replace("Artificial initialization duration took: ", "").strip())
    except TypeError:
        log("Could not parse Artificial Init Duration from lambda invocation log", ERROR)

    return 0


def get_available_threads(fn_log):
    available_threads_regex = re.compile("Available threads: \d*.\d*")
    try:
        if threads := re.search(available_threads_regex, fn_log):
            return int(threads.group().replace("Available threads: ", "").strip())
    except TypeError:
        log("Could not parse Available threads from lambda invocation log", ERROR)

    return 1


def get_fn_package_size_mb(fn_name):
    fn_package_identifier = get_fn_package_identifier(fn_name)
    try:
        image_details = run_executable(
            executable_path=describe_image_exec_path,
            args=[REPOSITORY_NAME, fn_package_identifier]
        )
        image_byte_size_regex = re.compile("\"imageSizeInBytes\": \\d*")
        if image_byte_size := re.search(image_byte_size_regex, image_details):
            image_bytes = int(image_byte_size.group().replace("\"imageSizeInBytes\": ", ""))
            return round(image_bytes / 1000 / 1000, 2)
    except TypeError:
        log("Could not get function image size. This might be because provided image name is wrong", ERROR)
    except CalledProcessError:
        log("Function is not deployed as image")

    try:
        s3_object_details = run_executable(
            executable_path=describe_s3_object_exec_path,
            args=[s3_bucket_name, fn_package_identifier]
        )
        s3_object_byte_size_regex = re.compile("\"ContentLength\": \\d*")
        if s3_object_bytes := re.search(s3_object_byte_size_regex, s3_object_details):
            package_bytes = int(s3_object_bytes.group().replace("\"ContentLength\": ", ""))
            return round(package_bytes / 1024 / 1024, 2)
    except TypeError:
        log("Could not get function zip package size. This might be because provided zip name is wrong", ERROR)

    return 0


def get_wait_for_response_duration(fn_log):
    wait_for_response_regex = re.compile("Wait for response duration: \d*.\d*")
    try:
        if wait_response_duration := re.search(wait_for_response_regex, fn_log):
            return float(wait_response_duration.group().replace("Wait for response duration: ", "").strip())
    except TypeError:
        log("Could not parse Available threads from lambda invocation log", ERROR)

    return 0


def get_layer_configuration_duration(fn_log):
    layer_configration_duration_regex = re.compile("Layer attachment duration: \d*.\d*")
    try:
        if layer_configuration_duration := re.search(layer_configration_duration_regex, fn_log):
            return float(layer_configuration_duration.group().replace("Layer attachment duration: ", "").strip())
    except TypeError:
        log("Could not parse Available threads from lambda invocation log", ERROR)

    return 0


def write_average_init_duration(test_num, results_path):
    if test_num == 't1':
        plot_by('function_code_package_size_mb', results_path, test_num)
    if test_num == 't2':
        plot_by('memory_size_mb', results_path, test_num)
    if test_num == 't3':
        plot_by('function_code_package_size_mb', results_path, test_num)
    if test_num == "t4":
        plot_by('function_code_package_size_mb', results_path, test_num)


def plot_by(by, results_path, test_num):
    result_files = get_results_path(results_path)

    data_frames = []
    for file in result_files:
        data_frames.append(read_csv_to_dataframe(results_path + file))
    df = pandas.concat(data_frames).round(2)

    df_filtered_grouped = df.groupby(by)
    plot(df_filtered_grouped, by, test_num)


def plot(df, xlabel, test_num):
    fig, ax = plt.subplots()
    ax.margins(x=0.15, y=0.25)

    lower_quantile_bound = .05
    upper_quantile_bound = .95
    for name, group in df:
        # if test_num == "t2":
        #     lower_artificial_init_quantile = group.artificial_init_duration.quantile(lower_quantile_bound)
        #     upper_artificial_init_quantile = group.artificial_init_duration.quantile(upper_quantile_bound)

            # group = group[(group.artificial_init_duration > 0)]
            # group = group[(group.artificial_init_duration >= lower_artificial_init_quantile) & (group.artificial_init_duration <= upper_artificial_init_quantile)]

        lower_init_duration_quantile = group.init_duration_ms.quantile(lower_quantile_bound)
        upper_init_duration_quantile = group.init_duration_ms.quantile(upper_quantile_bound)

        group = group[group.init_duration_ms > 0]
        group = group[(group.init_duration_ms >= lower_init_duration_quantile) & (group.init_duration_ms <= upper_init_duration_quantile)]

        plot_scatter_with_bars(ax, group, xlabel, test_num)
        # plot_memory_size_bars(ax, group, xlabel)

    # plot_std_line(ax, df)
    # plot_available_cpus(ax, df)

    if test_num == "t2":
        vCPU_f = lambda x: x / mem_per_1vCPU
        secax = ax.secondary_xaxis('top', functions=(vCPU_f, vCPU_f))
        secax.set_xlabel(translate('vcpu_for_memory'))

    title = translate('chart_title', genitive_case(xlabel))
    ax.set_title(title)
    ax.set_xlabel(translate(xlabel))
    ax.set_ylabel(translate('init_duration_ms'))
    ax.legend()

    x_keys = list(df.indices.keys())
    plt.xticks(x_keys, x_keys) # , rotation='vertical'
    plt.show()


def plot_scatter_with_bars(axes, group, xlabel, test_num):
    plot_scatter(axes, group, xlabel)
    plot_quantiles_bar(axes, group, xlabel, test_num, 0.30, 0.70)


def plot_scatter(axes, group, xlabel):
    axes.grid(zorder=0)
    axes.plot(
        getattr(group, xlabel),
        group.init_duration_ms, #group.wait_for_response_durations_ms + group.layer_configuration_duration_ms,
        marker='o',
        linestyle='',
        zorder=3,
        ms=2,
    )


def plot_quantiles_bar(axes, group, xlabel, test_num, lower_quantile, upper_quantile):
    lower_quantile_value = group.init_duration_ms.quantile(lower_quantile).round(2)
    upper_quantile_value = group.init_duration_ms.quantile(upper_quantile).round(2)

    group_x_value = getattr(group, xlabel).values[0]
    bar_spacing_x = 40 if test_num == "t2" else 10
    bar_width = 40 if test_num == "t2" else 10
    axes.bar(
        x=getattr(group, xlabel) - bar_spacing_x,
        width=bar_width,
        height=upper_quantile_value - lower_quantile_value,
        bottom=lower_quantile_value,
        align='edge',
        zorder=3,
        alpha=0.002
    )

    style = dict(size=6)

    # Quantiles
    # axes.text(group_x_value - 150, lower_quantile_value, lower_quantile, **style, ha='right')
    # axes.text(group_x_value - 150, upper_quantile_value, upper_quantile, **style, ha='right')

    # Quantile values
    bar_label_spacing_x = 40 if test_num == "t2" else 10
    bar_label_spacing_y = 80 if test_num == "t2" else 50
    axes.text(group_x_value - bar_spacing_x - bar_label_spacing_x, lower_quantile_value - bar_label_spacing_y, lower_quantile_value, **style, ha='left')
    axes.text(group_x_value - bar_spacing_x - bar_label_spacing_x, upper_quantile_value + bar_label_spacing_y, upper_quantile_value, **style, ha='left')


def plot_std_line(axes, df):
    axes.grid(zorder=0)
    axes.plot(
        df.init_duration_ms.std(),
        label=translate('init_duration_ms_std'),
        alpha=0.4,
        zorder=3,
        color='black'
    )


def plot_available_cpus(axes, df):
    axes.plot(
        df.available_threads.max(),
        label=translate('available_cpus'),
        alpha=0.4,
        color='black'
    )


def plot_memory_size_bars(ax, group, xlabel):
    lambda_init_duration = group.init_duration_ms - group.artificial_init_duration

    group_x_value = getattr(group, xlabel).values[0]

    bar_label_spacing_x = 0
    bar_label_spacing_y = 20
    # Lambda overhead init duration bar
    lambda_init_duration_height = lambda_init_duration.mean().round(2)
    ax.bar(
        x=getattr(group, xlabel),
        width=220,
        height=lambda_init_duration_height,
        bottom=0,
        alpha=0.1,
        color='orange',
    )
    style_1 = dict(size=6, color='black', ha='center', rotation=45)
    ax.text(group_x_value + bar_label_spacing_x, lambda_init_duration_height + bar_label_spacing_y, lambda_init_duration_height, **style_1)

    # Artificial init duration bar
    artificial_init_duration_height = group.artificial_init_duration.mean().round(2)
    ax.bar(
        x=getattr(group, xlabel),
        width=220,
        height=artificial_init_duration_height,
        bottom=lambda_init_duration.mean(),
        alpha=0.1,
        color='green',
    )

    style_2 = dict(size=6, color='black', ha='center', rotation=45)
    init_dur = (lambda_init_duration_height + artificial_init_duration_height).round(2)
    ax.text(group_x_value + bar_label_spacing_x, init_dur + bar_label_spacing_y, init_dur, **style_2)


def get_results_path(results_path):
    return [f for f in os.listdir(results_path) if isfile(join(results_path, f))]


if __name__ == "__main__":
    main()
