import csv
import xml.etree.ElementTree as etree

CSV_PATH = 'books.csv'
XML_PATH = 'currency.xml'

NAME_KEY = 'Название'
AUTHOR_KEY = 'Автор'
PRICE_KEY = 'Цена поступления'
YEAR_KEY = 'Дата поступления'
DAVAL_KEY = 'Кол-во выдач'


with open(CSV_PATH, encoding='windows-1251') as f:
    reader = csv.DictReader(f, delimiter = ';')
    name_count = sum(1 for row in reader if len(row[NAME_KEY]) > 30)
print('Task1: ', name_count)

##################################################

print('Task2:')

flag = 0

while not flag:
    required_author = input('Введите автора в формате Имя Фамилия, или пустую строку, чтобы выйти из поиска: ')
    if required_author == '':
        flag = 1
    else:
        with open(CSV_PATH, encoding='windows-1251') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if float(row[PRICE_KEY]) >= 150 and row[AUTHOR_KEY] == required_author:
                    print(row[NAME_KEY])

###############################################

total_books = 0

with open('task3output', 'w', encoding='utf-8') as output_file:
    with open(CSV_PATH, encoding='windows-1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if total_books < 20:
                book_info = f"{total_books} - {row[AUTHOR_KEY]} Дата поступления: {row[NAME_KEY]} ({row[YEAR_KEY]})\n"
                output_file.write(book_info)
                total_books += 1

print("Task3: 20 книг записаны в task3output.txt")

##############################################

print('Task4: ')
#Распарсить файл и извлечь данные, согласно варианту. Выполнить приведения типов по необходимости.

tree = etree.parse(XML_PATH)

root = tree.getroot()

values = []

for valute in root.findall('Valute'):
    value_elem = valute.find('Value')
    if value_elem is not None and value_elem.text:
        value = float(value_elem.text.replace(',', '.'))
        values.append(value)

average_value = sum(values) / len(values)
print(f"средний показатель value: {average_value:.4f}")

#############################

print('EXTRAS')

all_tags = set()
books_data = []

with open(CSV_PATH, encoding='windows-1251') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        if 'Жанр книги' in row and row['Жанр книги']:
            tags = row['Жанр книги'].split('#')
            for tag in tags:
                tag = tag.strip()
                if tag:
                    all_tags.add(tag)
        #########T2
        book_info = {
            'title': row.get(NAME_KEY, ''),
            'author': row.get(AUTHOR_KEY, ''),
            'popularity': int(row.get(DAVAL_KEY, 0)) 
        }
        books_data.append(book_info)

print("Теги:")
for i, tag in enumerate(sorted(all_tags), 1):
    print(f"{i}. {tag}")

print(f" тегов: {len(all_tags)}")

top_books = sorted(books_data, key=lambda x: x['popularity'], reverse=True)[:20]

print("Самые популярные 20 книг:")
for i, book in enumerate(top_books, 1):
    print(f"{i}. {book['author']} - '{book['title']}' (Выдач: {book['popularity']})")