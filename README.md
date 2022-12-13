# Проект парсинга pep

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка](#установка)
- [Справка по командам](#справка-по-командам)
- [Запуск](#запуск-парсера)
- [Автор](#автор)
- [Приложения](#приложения)


## Технологии
  - Парсинг данных (BeautifulSoup);
  - Кеширвание первичного запроса (Requests_cache);
  - Сбор логов на этапах парсинга (Logging);
  - Отслеживание переданных аргументов в командной строке (Argparse);
  - Вывод данных в формаие таблицы в консоль (PrettyTable);
  - Прогресс-бар для отслеживание процесса парсинга (Tqdm).

[⬆️Оглавление](#оглавление)


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
1. Клонировать репозиторий с GitHub:
```
git clone git@github.com:alexpro2022/bs4_parser_pep.git
```

2. Перейти в созданную директорию проекта:
```
cd bs4_parser_pep
```

3. Создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```

4. Установить все необходимые зависимости из файла **requirements.txt**:
```
pip install -r requirements.txt
```

5. Перейти в папку **src**:
```
cd src
```

[⬆️Оглавление](#оглавление)


## Справка по командам:
Вызывается командой -h или --help:
```
$ python main.py -h
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
```
$ python main.py latest-versions


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

```
$ python main.py latest-versions -o pretty


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
Данный вывод действителен только для режимов пп 1-3 (см. [описание работы](#описание-работы))

[⬆️Оглавление](#оглавление)


## Автор
[Aleksei Proskuriakov](https://github.com/alexpro2022)


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