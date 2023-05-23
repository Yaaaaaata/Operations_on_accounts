import datetime
import re


def filter_operations_by_status(data, status):
    """
    Фильтрует список операций по заданному статусу.
    """
    if isinstance(data, list):
        operations = data
        filtered_operations = [op for op in operations if op.get('state') == status]
        return filtered_operations
    elif isinstance(data, dict) and 'operations' in data:
        operations = data['operations']
        filtered_operations = [op for op in operations if op.get('state') == status]
        return filtered_operations
    else:
        print('Ошибка: данные не являются списком или словарем с ключом "operations"')
        return []


def sort_operations_by_date(operations, reverse=True):
    """
    Сортирует список операций по дате.
    """
    sorted_operations = sorted(operations, key=lambda op: op['date'], reverse=reverse)
    return sorted_operations


def mask_card_number(card_number):
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX.

    :param card_number: Номер карты.
    :type card_number: str
    :return: Маскированный номер карты.
    :rtype: str
    """
    if not card_number:
        return ''

    """Удаляем все символы, кроме цифр"""
    card_number = re.sub(r'\D', '', card_number)

    """Если длина номера карты больше 16 символов, оставляем только последние 4 цифры"""
    if len(card_number) > 16:
        card_number = '**{}'.format(card_number[-4:])
    else:
        """Добавляем пробелы между группами цифр"""
        card_number = ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])

    """Маскируем две последние группы цифр"""
    if len(card_number) == 19:
        card_number = '{}** **** {}'.format(card_number[:7], card_number[-4:])
    elif len(card_number) == 16:
        card_number = '{} **** {}'.format(card_number[:7], card_number[-4:])

    return card_number


def print_operations(operations):
    """
       Печатает отсортированный список операций.

       :param operations: Список словарей с данными об операциях.
       :type operations: list[dict[str, any]]
       """
    executed_operations = [op for op in operations if op.get('state') == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=lambda op: op['date'], reverse=True)
    for op in sorted_operations[:7]:
        date = datetime.datetime.strptime(op.get('date'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        description = op.get('description')
        from_ = op.get('from')
        to = op.get('to')
        amount = op.get('operationAmount', {}).get('amount')
        currency = op.get('operationAmount', {}).get('currency', {}).get('name')
        card_type = op.get('cardType')
        if card_type is not None:
            card_type = card_type.lower()
        else:
            card_type = ''
        if all([date, description, from_, to, amount, currency]):
            from_words = re.findall(r'[^\W\d_]+|\d+', from_)
            masked_from = ''
            for word_or_digit in from_words:
                if word_or_digit.isdigit():
                    if len(word_or_digit) > 16:
                        masked_from += '' + mask_card_number(word_or_digit) + ' '
                    elif len(word_or_digit) == 16:
                        masked_from += mask_card_number(word_or_digit)[:6] + ' ' + mask_card_number(word_or_digit)[6:] + ' '
                    else:
                        masked_from += mask_card_number(word_or_digit) + ' '
                else:
                    if re.match(r'^\d{4} \d{2}\*\*', word_or_digit):
                        masked_from += mask_card_number(word_or_digit)[:-2] + '** '
                    else:
                        masked_from += word_or_digit + ' '
            masked_to = ''
            if to.isdigit() and len(to) > 4:
                masked_to = '**** ' + to[-4:]
            else:
                masked_to = '**' + to[-4:]
            """Оставляем пробел между 4 цифрами"""
            masked_from = re.sub(r'(\d{4})\s(\d{2})\*\*\s', r'\1\2** ', masked_from)
            print(f"{date} {description}\n{masked_from}-> Счет {masked_to} \n{amount} {currency}\n")


if __name__ == '__main__':
    card_numbers = ['1234567812345670', '1234 5678 1234 5678', '1234-5678-1234-5678', '1234.5678.1234.5678']
    for card_number in card_numbers:
        print(mask_card_number(card_number))
