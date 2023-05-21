import os
import json
import zipfile
import argparse
from ..main import filter_operations_by_status, sort_operations_by_date, print_operations
import pytest


@pytest.fixture
def zip_path():
    # путь к файлу operations.zip на рабочем столе
    zip_file = 'C:/Users/Machenike/Desktop/operations.zip'
    yield zip_file


def test_zip_file(zip_path):
    """Тестирование функции zip_file из модуля main."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        json_path = os.path.join(zip_ref.extract('operations.json'))
        with open(json_path, encoding='utf-8') as json_file:
            operations = json.load(json_file)
        expected_keys = ['state', 'date', 'id', 'operationAmount', 'description', 'from', 'to']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('zip_path', help='path to the zip archive')
    args = parser.parse_args()
    test_zip_file(args.zip_path)


def test_filter_operations_by_status():
    """Тестирование функции filter_operations_by_status из модуля main."""
    data = [{'status': 'EXECUTED'}, {'status': 'PENDING'}, {'status': 'EXECUTED'}]
    result = filter_operations_by_status(data, 'EXECUTED')
    assert result == []


def test_sort_operations_by_date():
    """Тестирование функции sort_operations_by_date из модуля main."""
    data = [{'date': '2022-01-01'}, {'date': '2021-01-01'}, {'date': '2023-01-01'}]
    result = sort_operations_by_date(data)
    assert result == [{'date': '2023-01-01'}, {'date': '2022-01-01'}, {'date': '2021-01-01'}]


def test_print_operations(capsys):
    """Тестирование функции print_operations из модуля main."""
    data = [{'id': 1, 'name': 'Operation 1'}, {'id': 2, 'name': 'Operation 2'}]
    print_operations(data)
    captured = capsys.readouterr()
    assert captured.out == ''


