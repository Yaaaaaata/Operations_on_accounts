import argparse
import json
import zipfile
from utils import filter_operations_by_status, sort_operations_by_date, print_operations

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('zip_path', type=str, help='path to the zip file')
args = parser.parse_args()

try:
    with zipfile.ZipFile(args.zip_path, 'r') as zip_ref:
        if 'operations.json' not in zip_ref.namelist():
            print('File not found in archive')
            exit()
        zip_ref.extract('operations.json')
except FileNotFoundError:
    print('File not found')
    exit()

try:
    with open('operations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print('File not found')
    exit()
except json.JSONDecodeError:
    print('Invalid json format')
    exit()

try:
    executed_operations = filter_operations_by_status(data, 'EXECUTED')
except KeyError:
    print('Invalid data format')
    exit()

try:
    sorted_operations = sort_operations_by_date(executed_operations)
except ValueError:
    print('Invalid date format')
    exit()

try:
    print_operations(sorted_operations)
except TypeError:
    print('Invalid data format')
    exit()

