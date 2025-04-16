from irma import get_text

import os
import sys


def sort_one(file):
    records = get_text.outof(file), 'to records'
    for record in records:
        record_lines = sorted(record.splitlines())
        record = record_lines.joinlines()
    get_text.into(f'{file}_sorted.txt', 'from records', sorted(records))


def sort_many(files):
    print('Выполняется сортировка...')
    for file in files:
        sort_one(file)
        print(f'{file} отсортирован!')
    print('Готово')


if __name__ == "__main__":
    if len(sys.argv) > 0:
        p = sys.argv[1]
        if os.path.isdir(p):
            sort_many(p)
        elif os.path.isfile(p):
            sort_one(p)
        