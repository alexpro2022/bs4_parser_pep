import logging
import re
import requests_cache
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urljoin

from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    DOWNLOADS_URL,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    PEPS_URL,
    WHATS_NEW_URL,
)
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    response = get_response(session, WHATS_NEW_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', {'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', {'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all('li', {'class': 'toctree-l1'})

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_link = urljoin(WHATS_NEW_URL, section.find('a')['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1').text
        dl = find_tag(soup, 'dl').text.replace('\n', ' ')
        results.append((version_link, h1, dl))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    # pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    # pattern = r'\w+ (?P<version>\d\.\d+) \((?P<status>.*)\)'
    pattern = r'\w+ (\d\.\d+) \((.*)\)'
    for tag in a_tags:
        link = tag['href']
        text_match = re.match(pattern, tag.text)
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
    soup = BeautifulSoup(response.text, 'lxml')
    pattern = r'.+pdf-a4\.zip$'
    table_tag = find_tag(soup, 'table', {'class': 'docutils'})
    a4_pdf_tag = find_tag(table_tag, 'a', {'href': re.compile(pattern)})
    url = urljoin(DOWNLOADS_URL, a4_pdf_tag['href'])
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
        response.text, 'lxml',
        parse_only=SoupStrainer('section', id='numerical-index'),
    )
    for row in table.find_all('tr'):
        ref = row.find(class_='pep reference internal')
        if ref is None:
            continue
        pep_link = urljoin(PEPS_URL, ref['href'])
        response = get_response(session, pep_link)
        if response is None:
            continue
        rfc2822 = SoupStrainer('dl', class_='rfc2822 field-list simple')
        soup = BeautifulSoup(
            response.text, 'lxml',
            parse_only=rfc2822,
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
    for item in status_counter.items():
        results.append(item)
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
