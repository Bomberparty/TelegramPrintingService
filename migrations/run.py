import os
import sqlite3


CURRENT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def _get_files():
    migrations_path = f'{CURRENT_PATH}/schemes'

    for file in os.listdir(migrations_path):
        if os.path.isfile(os.path.join(migrations_path, file)):
            yield file  # елда, чтобы не жрало оперативку, когда будет много файлов


def _run_migration(file_path):
    # Тут просто читаем файл и передаём его как стейтмент

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    with open(file_path, 'r') as f:
        stmt = f.read().replace('\n', ' ')

    cur.execute(stmt)
    con.commit()
    con.close()


def run_migrations():
    # Получаем последнюю версию бд
    current_version_path = f'{CURRENT_PATH}/current_version'
    with open(current_version_path, 'r') as f:
        current_version = int(f.read())

    # Чекаем, есть ли схема с версией больше, чем текущая
    for file in _get_files():
        last_version = int(file.split('_')[1].split('.')[0])
        if last_version > current_version:
            # Если есть, запускаем миграцию
            file_path = f'{CURRENT_PATH}/schemes/{file}'
            _run_migration(file_path)

        # Записываем номер миграции, которую только что запустили, т.к это последняя версия бд
        with open(current_version_path, 'w') as f:
            f.write(str(last_version))
