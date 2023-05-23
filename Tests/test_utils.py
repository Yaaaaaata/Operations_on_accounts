import pytest
from utils import filter_operations_by_status, sort_operations_by_date, mask_card_number, print_operations


def test_filter_operations_by_status():
    data = [
        {'id': 1, 'state': 'EXECUTED'},
        {'id': 2, 'state': 'PENDING'},
        {'id': 3, 'state': 'EXECUTED'},
        {'id': 4},
    ]
    assert filter_operations_by_status(data, 'EXECUTED') == [{'id': 1, 'state': 'EXECUTED'},
                                                             {'id': 3, 'state': 'EXECUTED'}]
    assert filter_operations_by_status(data, 'PENDING') == [{'id': 2, 'state': 'PENDING'}]
    assert filter_operations_by_status(data, 'UNKNOWN') == []


def test_sort_operations_by_date():
    operations = [
        {'id': 1, 'date': '2022-01-01T00:00:00.000Z'},
        {'id': 2, 'date': '2022-01-03T00:00:00.000Z'},
        {'id': 3, 'date': '2022-01-02T00:00:00.000Z'},
    ]
    assert sort_operations_by_date(operations) == [
        {'id': 2, 'date': '2022-01-03T00:00:00.000Z'},
        {'id': 3, 'date': '2022-01-02T00:00:00.000Z'},
        {'id': 1, 'date': '2022-01-01T00:00:00.000Z'},
    ]
    assert sort_operations_by_date(operations, reverse=False) == [
        {'id': 1, 'date': '2022-01-01T00:00:00.000Z'},
        {'id': 3, 'date': '2022-01-02T00:00:00.000Z'},
        {'id': 2, 'date': '2022-01-03T00:00:00.000Z'},
    ]


def test_mask_card_number():
    card_numbers = [
        ('1234567812345670', '1234 56** **** 5670'),
        ('1234 5678 1234 5678', '1234 56** **** 5678'),
        ('1234-5678-1234-5678', '1234 56** **** 5678'),
        ('1234.5678.1234.5678', '1234 56** **** 5678'),
        ('', ''),
    ]
    for card_number, expected in card_numbers:
        assert mask_card_number(card_number) == expected


@pytest.fixture
def operations():
    return [
        {
            'state': 'EXECUTED',
            'date': '2022-01-01T12:00:00.000000',
            'description': 'Payment',
            'from': '1234567812345678',
            'to': '9876543210987654',
            'operationAmount': {
                'amount': 1000,
                'currency': {'name': 'USD'}
            },
            'cardType': 'VISA'
        },
        {
            'state': 'EXECUTED',
            'date': '2022-01-02T12:00:00.000000',
            'description': 'Transfer',
            'from': '9876543210987654',
            'to': '1234567812345678',
            'operationAmount': {
                'amount': 2000,
                'currency': {'name': 'EUR'}
            },
            'cardType': None
        },
        {
            'state': 'PENDING',
            'date': '2022-01-03T12:00:00.000000',
            'description': 'Withdrawal',
            'from': None,
            'to': '1111222233334444',
            'operationAmount': {
                'amount': 500,
                'currency': {'name': 'GBP'}
            },
            'cardType': 'MASTERCARD'
        }
    ]


def test_print_operations(operations, capsys):
    print_operations(operations)
    captured = capsys.readouterr()
    assert captured.out == (
        "02.01.2022 Transfer\n9876 5 4** **** 7654 -> Счет **** 5678 \n2000 EUR\n\n"
        "01.01.2022 Payment\n1234 5 6** **** 5678 -> Счет **** 7654 \n1000 USD\n\n"
    )
