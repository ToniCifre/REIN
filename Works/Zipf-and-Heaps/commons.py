import re
import csv


def read_csv(file_name):
    import csv
    with open(file_name + '.csv', 'r', ) as file:
        reader = csv.reader(file)
        return [[int(row[0]), row[1]] for row in reader if row]


def write_csv(csv_rowlist, file_name):
    with open(file_name + '.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_rowlist)


def clean_words(words):
    aux = []
    pattern = re.compile("[A-Za-z][a-z'a-z]{2,9}")
    for row in words:
        if pattern.match(row[1]) and int(row[0]) >= 4:
            aux.append(row)

    print(f'{len(words) - len(aux)} words removed.')
    return aux