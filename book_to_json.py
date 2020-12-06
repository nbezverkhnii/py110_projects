import re
import os
import json
import argparse

# Информация о каждой книге замкнута между #### и [Amazon.com]
BOOK_PATTERN = re.compile(r'(?<=#### )(.*?)(?<=\[Amazon.com\])', re.DOTALL)
ITEMS_PATTERN = re.compile(r"(?P<position>^(?:\d{1,2}))\.\s+\["
                            "(?P<book>.+?)\]\("
                            "(?P<book_url>.+?)\)\s+by\s+"
                            "(?P<author>([\w\s'&\.]+))\s\("
                            "(?P<recommended>\d{,3}\.\d{,3})\%\s+recommended\).+\("
                            "(?P<cover_url>.*?)\).*\""
                            "(?P<description>.*?)\"", 
                            flags=re.DOTALL | re.UNICODE)


def create_parser() -> None:
    """
    Парсер аргументов командной строки.
    Необязательные аругменты: 
    indent - аргумент indent метода json.dump()
    output_name - имя файла, который будет сохранен в результате
    Если имя файла не задается пользователем, то файл будет называться
    также, как и файл, который подается на вход.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Имя файла, который содержит список книг')
    parser.add_argument('-i', '--indent',
                        type=int,
                        default=4,
                        help='Параметр отступа indent в JSON файле')
    parser.add_argument('-o','--output_name',
                        default='books',
                        help='Имя JSON файла')
    return parser


def re_parser(text: str) -> list:
    """
    Парсер текста.    
    Разбивает текст на отдельные книги.
    Отдельные книги разбивает на категории.
    Сортирует полученный список словарей
    в порядке убывания их популярности по ключу 'recommended'
    
    Parameters:
    text: str - строка, которая содежит весь текст файла, 
    подаваемого на вход программы скрипта.
    
    Returns:
    result: list - список словарей, содержащих информацию о книгах.
    """
    books_item_list = []
    
    for book in BOOK_PATTERN.findall(text):
        for items in ITEMS_PATTERN.finditer(book):
            books_item_list.append(items.groupdict())
            
    result = sorted(books_item_list,  
                    key=lambda x: float(x['recommended']), 
                    reverse=True)
    
    return result


def create_json(output_filename: str, result_books_list: list, indent: int) -> None:
    """
    Записывает result_books_list в JSON файл
    
    Parameters:
    output_filename: str - имя файла, который будет сохранен
    result_books_list: list - список словарей, с информацией о книгах
    indent: int - параметр indent метода json.dump()
    """
    with open(output_filename, 'w') as file:
        json.dump(result_books_list, file, indent=indent, ensure_ascii=False)      
                     
        
def main() -> None:
    """
    Парсер текста.
    Принимает агрументы командной строки.
    Открывает и читает текст из файла.
    Переименовывает выходной файл, если это нужно.
    """
    parser = create_parser()
    args = parser.parse_args()
    filename = args.filename
    indent = args.indent
    output_name = args.output_name
                
    with open(filename, 'rt') as input_file:
        text = input_file.read()
        
        # Потому что необходимо записать .json файл
        name, ext = os.path.splitext(filename)
        output_filename = name + '.json'
        
        # Если пользователь ввел имя JSON-файла, то возьмем его
        if output_name != 'books':
            if not output_name.endswith('.json'):
                output_name += '.json'
            output_filename = output_name
            
        result_books_list = re_parser(text)
        create_json(output_filename, result_books_list, indent)
    
            
if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print('Вы пытаетесь открть несуществующий файл!')
    