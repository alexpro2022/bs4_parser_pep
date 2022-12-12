import csv
import logging
from datetime import datetime as dt

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    if cli_args.output == 'pretty':
        pretty_output(results)
    elif cli_args.output == 'file':
        file_output(results, cli_args)
    else:
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
    filename = f'{cli_args.mode}_{dt.now().strftime(DATETIME_FORMAT)}'
    path = results_dir / (filename + '.csv')
    with open(path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {path}')
