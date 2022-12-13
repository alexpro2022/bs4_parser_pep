from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
LOGS = BASE_DIR / 'logs'
MAIN_DOC_URL = 'https://docs.python.org/3/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')
PEPS_URL = 'https://peps.python.org/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
ENCODING = 'utf-8'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
PARSER = 'lxml'

# шаблон для поиска zip-архива с документами в формате PDF (A4 paper size)
DOWNLOAD_PATTERN = r'.+pdf-a4\.zip$'

# шаблон поиска версий и их статусов например Python 3.10 (stable)
VERSION_PATTERN = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'


class HTMLTag:
    A = 'a'
    CLASS = 'class'
    DIV = 'div'
    HREF = 'href'
    ID = 'id'
    SECTION = 'section'
