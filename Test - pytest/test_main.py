import os
import json
import zipfile
from main import filter_operations_by_status, sort_operations_by_date, print_operations
import argparse


def test_zip_file(zip_path):
    # создаем временный файл для теста
    with zipfile.ZipFile('test.zip', 'w') as zip_ref:
        zip_ref.writestr('operations.json', json.dumps([{'status': 'EXECUTED', 'date': '2021-01-01'}]))
    # запускаем тестируемую функцию
    os.system(f'python main.py {zip_path}')
    # удаляем временные файлы
    os.remove('test.zip')
    os.remove('operations.json')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('zip_path', help='path to the zip archive')
    args = parser.parse_args()
    test_zip_file(args.zip_path)


def test_filter_operations_by_status():
    data = [{'status': 'EXECUTED'}, {'status': 'PENDING'}, {'status': 'EXECUTED'}]
    result = filter_operations_by_status(data, 'EXECUTED')
    assert result == [{'status': 'EXECUTED'}, {'status': 'EXECUTED'}]


def test_sort_operations_by_date():
    data = [{'date': '2022-01-01'}, {'date': '2021-01-01'}, {'date': '2023-01-01'}]
    result = sort_operations_by_date(data)
    assert result == [{'date': '2021-01-01'}, {'date': '2022-01-01'}, {'date': '2023-01-01'}]


def test_print_operations(capsys):
    data = [{'id': 1, 'name': 'Operation 1'}, {'id': 2, 'name': 'Operation 2'}]
    print_operations(data)
    captured = capsys.readouterr()
    assert captured.out == '1: Operation 1\n2: Operation 2\n'

