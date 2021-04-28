import csv
import os
import pandas


def read_file(path):
    with open(path, 'r') as file:
        data = file.read()

    return data


def write_to_file(data, path, mode='w'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as f:
        if type(data) == list:
            for item in data:
                f.write('%s\n' % item)

        if type(data) == str:
            f.write(data)


def write_to_csv(data, header, path, mode='w'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)


def read_csv(path):
    results = []
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results.append(row)

    return results


def read_csv_to_dataframe(path):
    return pandas.read_csv(path, delimiter=',')
