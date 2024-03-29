import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import DATETIME_FORMAT, ENCODING, LOG_FORMAT, LOGS


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    LOGS.mkdir(exist_ok=True)
    log_file = LOGS / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5, encoding=ENCODING)
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
