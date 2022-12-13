import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOAD_PATTERN, DOWNLOADS_URL,
                       EXPECTED_STATUS, MAIN_DOC_URL, PARSER, PEPS_URL,
                       VERSION_PATTERN, WHATS_NEW_URL, HTMLTag)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    response = get_response(session, WHATS_NEW_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, PARSER)
    main_div = find_tag(
        soup, HTMLTag.SECTION, {HTMLTag.ID: 'what-s-new-in-python'})
    div_with_ul = find_tag(
        main_div, HTMLTag.DIV, {HTMLTag.CLASS: 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', {HTMLTag.CLASS: 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_link = urljoin(
            WHATS_NEW_URL, section.find(HTMLTag.A)[HTMLTag.HREF])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, PARSER)
        h1 = find_tag(soup, 'h1').text
        dl = find_tag(soup, 'dl').text.replace('\n', ' ')
        results.append((version_link, h1, dl))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, PARSER)
    sidebar = find_tag(
        soup, HTMLTag.DIV, {HTMLTag.CLASS: 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all(HTMLTag.A)
            break
    else:
        raise Exception('Не найден список c версиями Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    for tag in a_tags:
        link = tag[HTMLTag.HREF]
        text_match = re.match(VERSION_PATTERN, tag.text)
        if text_match is None:
            version, status = tag.text, ''
        else:
            version, status = text_match.groups()
        results.append((link, version, status))
    return results


def download(session):
    response = get_response(session, DOWNLOADS_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, PARSER)
    table_tag = find_tag(soup, 'table', {HTMLTag.CLASS: 'docutils'})
    a4_pdf_tag = find_tag(
        table_tag, HTMLTag.A, {HTMLTag.HREF: re.compile(DOWNLOAD_PATTERN)})
    url = urljoin(DOWNLOADS_URL, a4_pdf_tag[HTMLTag.HREF])
    filename = url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    path = downloads_dir / filename
    response = session.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {path}')


def pep(session):
    status_counter = {}
    response = get_response(session, PEPS_URL)
    if response is None:
        return
    table = BeautifulSoup(
        response.text, PARSER,
        parse_only=SoupStrainer(HTMLTag.SECTION, id='numerical-index'),
    )
    for row in table.find_all('tr'):
        ref = row.find(class_='pep reference internal')
        if ref is None:
            continue
        pep_link = urljoin(PEPS_URL, ref[HTMLTag.HREF])
        response = get_response(session, pep_link)
        if response is None:
            continue
        soup = BeautifulSoup(
            response.text, PARSER,
            parse_only=SoupStrainer(
                'dl', class_='rfc2822 field-list simple'),
        )
        cart_status = soup.find(
            string='Status').parent.find_next_sibling().text
        expected_status = EXPECTED_STATUS[row.find('td').text[1:]]
        if cart_status not in expected_status:
            logging.info(
                f'Несовпадающие статусы:\n'
                f'{pep_link}\n'
                f'Статус в карточке: {cart_status}\n'
                f'Ожидаемые статусы: {expected_status}\n'
            )
        status_counter[cart_status] = status_counter.get(cart_status, 0) + 1
    results = [('Статус', 'Количество')]
    for key, value in status_counter.items():
        results.append((key, value))
    total = sum(status_counter.values())
    results.append(('Total', total))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    parser_mode = args.mode
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
