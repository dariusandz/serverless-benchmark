import sys
from subprocess import check_output


def run_executable(executable_path, args=[]):
    result = check_output([executable_path] + args)
    return result.decode(sys.stdout.encoding)
