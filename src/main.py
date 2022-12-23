import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup, SoupStrainer
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOAD_PATTERN, DOWNLOADS_URL,
                       EXPECTED_STATUS, LATEST_VERSIONS_SIDEBAR, MAIN_DOC_URL,
                       PARSER, PEP_NUMERICAL_INDEX, PEP_PAGE_CART,
                       PEP_REFERENCE, PEPS_URL, VERSION_PATTERN,
                       WHATS_NEW_SECTION, WHATS_NEW_URL, HTMLTag)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    response = get_response(session, WHATS_NEW_URL)
    if response is None:
        return
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    main_section = BeautifulSoup(
        response.text, PARSER,
        parse_only=SoupStrainer(
            HTMLTag.SECTION,
            {HTMLTag.ID: WHATS_NEW_SECTION}
        )
    )
    sections_by_python = find_tag(
        main_section, HTMLTag.DIV,
        {HTMLTag.CLASS: 'toctree-wrapper'}
    )(HTMLTag.LI, {HTMLTag.CLASS: 'toctree-l1'})

    for section in tqdm(sections_by_python):
        version_link = urljoin(
            WHATS_NEW_URL,
            section.find(HTMLTag.A)[HTMLTag.HREF]
        )
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
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    sidebar_ul_tags = BeautifulSoup(
        response.text, PARSER,
        parse_only=SoupStrainer(
            HTMLTag.DIV, {HTMLTag.CLASS: LATEST_VERSIONS_SIDEBAR}
        )
    )(HTMLTag.UL)

    for ul in sidebar_ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul(HTMLTag.A)
            break
    try:
        for tag in a_tags:
            link = tag[HTMLTag.HREF]
            text_match = re.match(VERSION_PATTERN, tag.text)
            if text_match is None:
                version, status = tag.text, ''
            else:
                version, status = text_match.groups()
            results.append((link, version, status))
    except UnboundLocalError:
        raise ParserFindTagException('Не найден список c версиями Python')
    return results


def download(session):
    response = get_response(session, DOWNLOADS_URL)
    if response is None:
        return
    table = BeautifulSoup(
        response.text, PARSER,
        parse_only=SoupStrainer(HTMLTag.TABLE, class_='docutils')
    )
    a4_pdf_tag = find_tag(
        table, HTMLTag.A,
        {HTMLTag.HREF: re.compile(DOWNLOAD_PATTERN)}
    )
    url = urljoin(DOWNLOADS_URL, a4_pdf_tag[HTMLTag.HREF])
    filename = url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    path = downloads_dir / filename
    # DOWNLOADS.mkdir(exist_ok=True)
    # path = DOWNLOADS / filename
    response = get_response(session, url)
    if response is None:
        return
    with open(path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {path}')


def pep(session):
    response = get_response(session, PEPS_URL)
    if response is None:
        return
    status_counter = {}
    table_rows = BeautifulSoup(
        response.text, PARSER,
        parse_only=SoupStrainer(HTMLTag.SECTION, id=PEP_NUMERICAL_INDEX)
    ).find('tbody')(HTMLTag.TR)

    for row in table_rows:
        ref = row.find(class_=PEP_REFERENCE)
        pep_link = urljoin(PEPS_URL, ref[HTMLTag.HREF])
        response = get_response(session, pep_link)
        if response is None:
            continue
        cart_status = BeautifulSoup(
            response.text, PARSER,
            parse_only=SoupStrainer(HTMLTag.DL, class_=PEP_PAGE_CART)
        ).find(string='Status').parent.find_next_sibling().text
        expected_status = EXPECTED_STATUS[row.find(HTMLTag.TD).text[1:]]
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
    results.append(('Total', sum(status_counter.values())))
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
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION)
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    results = MODE_TO_FUNCTION[args.mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
