# Проект парсинга pep
[![status](https://github.com/alexpro2022/bs4_parser_pep/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/bs4_parser_pep/actions)
[![codecov](https://codecov.io/gh/alexpro2022/bs4_parser_pep/branch/master/graph/badge.svg?token=WTVTVN092K)](https://codecov.io/gh/alexpro2022/bs4_parser_pep)

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка](#установка)
- [Справка по командам](#справка-по-командам)
- [Запуск](#запуск)
- [Автор](#автор)
- [Приложения](#приложения)


## Технологии
<details><summary>Развернуть</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)
[![argparse](https://img.shields.io/badge/-argparse-464646?logo=python)](https://docs.python.org/3/howto/argparse.html)
[![csv](https://img.shields.io/badge/-csv-464646?logo=python)](https://docs.python.org/3/library/csv.html)
[![datetime](https://img.shields.io/badge/-datetime-464646?logo=python)](https://docs.python.org/3/library/datetime.html)
[![enum](https://img.shields.io/badge/-enum-464646?logo=python)](https://docs.python.org/3/library/enum.html)
[![logging](https://img.shields.io/badge/-logging-464646?logo=python)](https://docs.python.org/3/library/logging.html)
[![pathlib](https://img.shields.io/badge/-pathlib-464646?logo=python)](https://docs.python.org/3/library/pathlib.html)
[![re](https://img.shields.io/badge/-re-464646?logo=python)](https://docs.python.org/3/library/re.html)
[![urllib](https://img.shields.io/badge/-urllib-464646?logo=python)](https://docs.python.org/3/library/urllib.html)

[![PrettyTable](https://img.shields.io/badge/-Pretty_Table-464646?logo=prettytable)](https://pypi.org/project/prettytable/)
[![Requests_cache](https://img.shields.io/badge/-Requests--Cache-464646?logo=requests-cache)](https://requests-cache.readthedocs.io/en/stable/)
[![Tqdm](https://img.shields.io/badge/-Tqdm-464646?logo=Tqdm)](https://github.com/tqdm/tqdm)


**Парсинг - библиотеки и модули:**

[![Beautiful_Soup](https://img.shields.io/badge/-Beautiful_Soup_4-464646?logo=bs4)](https://beautiful-soup-4.readthedocs.io/en/latest/)


**Тестирование:**

[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)


**CI/CD:**

[![GitHub](https://img.shields.io/badge/-GitHub-464646?logo=GitHub)](https://docs.github.com/en)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)
</details>

## Описание работы
Парсер работает в 4-х режимах (каждый режим обрабатывается одноименной функцией):
1. сбор версий языка и их авторов - `whats_new`
2. сбор информации о версиях - `latest_versions`
3. сбор информации о стандартах PEP - `pep`
4. скачивание документации - `download`

Работа каждой функции осуществляется путём её вызова в консоли. 
При вызове функции из п.1-3 возможны различные представления вывода информации:
- стандартный вывод в консоль; 
- вывод в консоль, оформленный в виде таблицы;
- сохранение вывода в **.csv**-файл (помещается в папку **results** (см. <a href="#t1">Структура проекта</a>))

При вызове функции скачивания документации (п.4) zip-архив сохраняется в папке **downloads** (см. <a href="#t1">Структура проекта</a>))

[⬆️Оглавление](#оглавление)


## Установка:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE (например VSCode).
1. Клонировать репозиторий с GitHub:
```
git clone https://github.com/alexpro2022/bs4_parser_pep.git && cd bs4_parser_pep
```

2. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```
    python -m venv venv && source venv/Scripts/activate
   ```

3. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```
python -m pip install --upgrade pip && pip install -r requirements.txt
```

4. Перейдите в папку **src**:
```
cd src
```

[⬆️Оглавление](#оглавление)


## Справка по командам:
Вызывается командой -h или --help:
```
python main.py -h
```

Выводится описание парсера, и его аргументы:
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

options:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

[⬆️Оглавление](#оглавление)


## Запуск:
Осуществляется по команде `python main.py` и добавлений нужной функции режима работы, например:
```bash
python main.py latest-versions
```
```bash
"2022-12-13_17-49-40 - [INFO] - Парсер запущен!"
"2022-12-13_17-49-40 - [INFO] - Аргументы командной строки: Namespace(mode='latest-versions', clear_cache=False, output=None)"
Ссылка на документацию Версия Статус
https://docs.python.org/3.12/ 3.12 in development
https://docs.python.org/3.11/ 3.11 stable
https://docs.python.org/3.10/ 3.10 stable
https://docs.python.org/3.9/ 3.9 security-fixes
https://docs.python.org/3.8/ 3.8 security-fixes
https://docs.python.org/3.7/ 3.7 security-fixes
https://docs.python.org/3.6/ 3.6 EOL
https://docs.python.org/3.5/ 3.5 EOL
https://docs.python.org/2.7/ 2.7 EOL
https://www.python.org/doc/versions/ All versions 
"2022-12-13_17-49-40 - [INFO] - Парсер завершил работу."
```
<a href="#t2">Смотри замечание</a>

При использвании доп. команд (`-o pretty` или `-o file`) вывод будет либо оформлен в виде таблицы и
выведен в консоль, либо сохранён файлом с расширеним **.csv** соответственно:

```bash
python main.py latest-versions -o pretty
```
```bash
"2022-12-13_17-51-41 - [INFO] - Парсер запущен!"
"2022-12-13_17-51-41 - [INFO] - Аргументы командной строки: Namespace(mode='latest-versions', clear_cache=False, output='pretty')"
+--------------------------------------+--------------+----------------+
| Ссылка на документацию               | Версия       | Статус         |
+--------------------------------------+--------------+----------------+
| https://docs.python.org/3.12/        | 3.12         | in development |
| https://docs.python.org/3.11/        | 3.11         | stable         |
| https://docs.python.org/3.10/        | 3.10         | stable         |
| https://docs.python.org/3.9/         | 3.9          | security-fixes |
| https://docs.python.org/3.8/         | 3.8          | security-fixes |
| https://docs.python.org/3.7/         | 3.7          | security-fixes |
| https://docs.python.org/3.6/         | 3.6          | EOL            |
| https://docs.python.org/3.5/         | 3.5          | EOL            |
| https://docs.python.org/2.7/         | 2.7          | EOL            |
| https://www.python.org/doc/versions/ | All versions |                |
+--------------------------------------+--------------+----------------+
"2022-12-13_17-51-41 - [INFO] - Парсер завершил работу."

```
<a href="#t2">Смотри замечание</a>  
<hr>  

<h4 id="t2">Замечание</h4>  
Данный вывод действителен только для режимов пп 1-3, смотри 

[Описание работы](#описание-работы)

[⬆️Оглавление](#оглавление)


## Автор
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️Оглавление](#оглавление)

## Приложения:
<details open>
  <summary>
    <h3 id="t1"> Структура проекта </h3>
  </summary>

```cmd
bs4_parser_pep:
|   .flake8
|   .gitignore
|   pytest.ini
|   README.md
|   requirements.txt
|
+---src
|   |   configs.py  <-- конфигуратор команд командной строки, логов
|   |   constants.py  <-- Дефолтные ссылки, форматы, пути и т.д.
|   |   exceptions.py  <-- Кастомные исключения
|   |   main.py  <-- Основная логика парсера
|   |   outputs.py  <-- Обработчик вывода ф-ий
|   |   utils.py  <-- Обработчик ошибок
|   |   __init__.py
|   |   
|   +---downloads  <-- директория для сохранения zip-архивов
|   |
|   +---logs  <-- директория для хранения логов
|   |
|   +---results  <-- директория для сохранения csv-файлов
|   |
|   \---__pycache__
|
+---tests  <-- Тесты, активирующиеся по команде pytest из корневой директории
|
\---venv

```
</details>

[⬆️В начало](#Проект-парсинга-pep)
