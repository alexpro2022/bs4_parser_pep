import csv
import logging
from datetime import datetime as dt
from enum import Enum

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, ENCODING


class OutputType(str, Enum):
    PRETTY = 'pretty'
    FILE = 'file'


def control_output(results, cli_args):
    match cli_args.output:
        case OutputType.PRETTY:
            pretty_output(results)
        case OutputType.FILE:
            file_output(results, cli_args)
        case _:
            default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable(results[0], align='l')
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    filename = f'{cli_args.mode}_{dt.now().strftime(DATETIME_FORMAT)}.csv'
    path = results_dir / filename
    with open(path, 'w', encoding=ENCODING) as file:
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {path}')
