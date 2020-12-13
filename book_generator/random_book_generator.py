import re 
import json
import pandas as pd
import random
import argparse
from faker import Faker
from typing import ClassVar, Callable
from itertools import cycle
import conf

# Паттерн для поиска строк формата "Имя Фамилия"
AUTHOR_PATTERN = re.compile(r'[А-Я]\w+\s+[А-Я]\w+')


def create_parser() -> ClassVar:
    """
    Парсер аргументов командной строки
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('count',
                        type=int, 
                        help='Количество случайных элементов, которое необходимо сгенерировать')
    parser.add_argument('-p','--pk',
                        type=int,
                        default=1,
                        help='Порядкой номер первой генерируемой книги')
    parser.add_argument('-a', '--authors',
                         type=int, 
                         help='Количество авторов для каждого элемента')
    parser.add_argument('-s', '--sale',
                        action='store_true', 
                        default=False,
                        help='Генерировать скидку')
    
    subparsers = parser.add_subparsers(dest='command')
    subparser_json(subparsers)
    subparser_csv(subparsers)
    
    return parser
    
    
def subparser_json(subparsers) -> Callable:
    """
    Сабпарсер для вывода в JSON
    """
    json_parser = subparsers.add_parser('json',
                                         help='Режим вывода в JSON')
    
    json_parser.add_argument('-j', '--json_filename',
                             dest='json_filename', 
                             required=True,
                             help='Имя файла для вывода результата')    
    json_parser.add_argument('-i','--indent',
                             type=int, 
                             default=1,
                             help='Количество отступов JSON')
    
    return json_parser


def subparser_csv(subparsers) -> Callable:
    """
    Сабпарсер для вывода в CSV
    """
    csv_subparser = subparsers.add_parser('csv',
                                          help='Режим вывода в CSV')
    csv_subparser.add_argument('-v', '--csv_filename',
                               dest='csv_filename', 
                               required=True,
                               help='Имя файла для вывода результата')  
    csv_subparser.add_argument('-n','--newline',
                               type=str, 
                               default='\n',
                               help='Разделитель строк')
    csv_subparser.add_argument('-d','--delimiter',
                               type=str, 
                               default=',',
                               help='Разделитель элементов в строке')
    
    return csv_subparser


def random_author(number_of_author) -> list:
    """
    Выбирает случайный список атворов длиной number_of_author из файла conf.AUTHORS
    
    Еслм мы заранее не знаем сколько строк в файле conf.AUTHORS,
    то зацикливаем его с помощью itertools.cycle(). Тогда
    в random_lines могут лежать номера строк из дапазона, верхняя 
    граница которого больше, чем количество строк в файле.
    """
    # количество элементов в два раза первышает number_of_author
    # чтобы authors точно заполнился до нужного количества элементов = number_of_author
    random_lines = random.sample(range(0,1000), 2*number_of_author)
    
    # set() выбран, чтобы в authors не встретилось повторяющихся имен
    authors = set()
    
    with open(conf.AUTHORS, 'rt') as file:
        current_line = 0
        cycle_file = cycle(file)
        while len(authors) < number_of_author:
            line = next(cycle_file)
            if not AUTHOR_PATTERN.search(line):
                raise ValueError("Файл содержит строку, не совпадающую с паттерном")
            if AUTHOR_PATTERN.search(line) and current_line in random_lines:
                authors.add(line.strip())
            current_line += 1

    return list(authors)
    

def random_title() -> str:
    """
    Выбирает случейное название книги из файла conf.TITLES
    """
    random_line = random.randint(0, 1000)
    i = 0
    
    with open(conf.TITLES, 'rt') as file:
        cycle_file = cycle(file)
        result = ''
        
        while result == '':
            line = next(cycle_file)
            if i == random_line:
                result = line.strip()
            i += 1

    return result
        
    
def random_isbn13() -> str:
    """
    Генерирует случайный номер ISBN
    """
    faker = Faker()
    return faker.isbn13()
    

def random_book(pk: int = 1) -> dict:
    """
    Генерирует случайную книгу
    """    
    while True:
        model = conf.MODEL
        pk = pk
        title = random_title()
        year = random.randint(1800, 2020)
        page = random.randint(2, 3000)
        isbn13 = random_isbn13()
        rating =  round(random.uniform(0, 5),1)
        price = round(random.uniform(1, 10000),2)
        discount = random.randint(1, 100)
        number_of_author = random.randint(1, 3)
        author = random_author(number_of_author)

        one_book = {"model": model,
                    "pk": pk,
                    "fields": {"title": title,
                               "year": year,
                               "pages": page,
                               "isbn13": random_isbn13(),
                               "rating": rating,
                               "price": price,
                               "discount": discount,
                               "author": author,
                    }

        }
        
        yield one_book
        pk += 1 
        
        
def create_json(output_file: str, result_books_list: list, indent: int) -> None:
    """
    Записывает result_books_list в JSON файл
    
    Parameters:
    output_file: str - имя файла, который будет сохранен
    result_books_list: list - список словарей, с информацией о книгах
    indent: int - параметр indent метода json.dump()
    """
    if not output_file.endswith('.json'):
        output_file += '.json'
        
    with open(output_file, 'w') as file:
        json.dump(result_books_list, 
                  file, 
                  indent=indent, 
                  ensure_ascii=False) 
        

def create_csv(output_file: str, 
               result_books_list: list, 
               delimiter: str,
               newline: str) -> None:
    """
    Записывает result_books_list в CSV файл
    
    Parameters:
    output_file: str - имя файла, который будет сохранен
    result_books_list: list - список словарей, с информацией о книгах 
    delimiter: str - резделитель значений в строке
    newline: str - резделитель строк 
    """
    if not output_file.endswith('.csv'):
        output_file += '.csv'
            
    pd.DataFrame(result_books_list).set_index('pk').to_csv(output_file, 
                                                           sep=delimiter, 
                                                           line_terminator=newline)
    
    
def main() -> None:
    """
    Основная функция программы 
    """
    parser = create_parser()
    args = parser.parse_args()
    
    count = args.count
    command = args.command
    pk = args.pk
    
    book_gen = random_book(pk)
    
    if args.command == None:
        for _ in range(count):
            print(next(book_gen))
    elif args.command == 'json':
        result_books_list = [next(book_gen) for _ in range(count)]
        create_json(args.json_filename, result_books_list, args.indent)
    elif args.command == 'csv':
        result_books_list = [next(book_gen) for _ in range(count)]
        create_csv(args.csv_filename, result_books_list, args.delimiter, args.newline)


if __name__ == '__main__':
    main()
