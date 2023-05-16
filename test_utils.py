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
        ('1234567812345670', '1234 5678 12** ****'),
        ('1234 5678 1234 5678', '1234 5678 12** ****'),
        ('1234-5678-1234-5678', '1234 5678 12** ****'),
        ('1234.5678.1234.5678', '1234 5678 12** ****'),
        ('', ''),
    ]
    for card_number, expected in card_numbers:
        assert mask_card_number(card_number) == expected


def test_print_operations(capsys):
    operations = [
        {
            'id': 1,
            'date': '2022-01-01T00:00:00.000Z',
            'description': 'Payment',
            'from': '1234567812345670',
            'to': '9876543210987654',
            'operationAmount': {'amount': 100, 'currency': {'name': 'RUB'}},
            'state': 'EXECUTED',
            'cardType': 'VISA',
        },
        {
            'id': 2,
            'date': '2022-01-02T00:00:00.000Z',
            'description': 'Transfer',
            'from': '9876543210987654',
            'to': '1234567812345670',
            'operationAmount': {'amount': 50, 'currency': {'name': 'USD'}},
            'state': 'EXECUTED',
            'cardType': 'MASTERCARD',
        },
        {
            'id': 3,
            'date': '2022-01-03T00:00:00.000Z',
            'description': 'Withdrawal',
            'from': '1234567812345670',
            'to': '',
            'operationAmount': {'amount': 200, 'currency': {'name': 'EUR'}},
            'state': 'PENDING',
            'cardType': '',
        },
    ]
    print_operations(operations)
    captured = capsys.readouterr()
    assert captured.out == (
        "03.01.2022 Withdrawal\n1234 5678 12** ****-> Счет \n200 EUR\n"
        "02.01.2022 Transfer\n**** **** **** 7654-> Счет 1234 5678 \n50 USD\n"
        "01.01.2022 Payment\n1234 5678 12** ****-> Счет **** **** **** 7654 \n100 RUB\n"
    )



