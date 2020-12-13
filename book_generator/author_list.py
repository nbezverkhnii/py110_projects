from faker import Faker


def main(n: int=1000) -> None:
    """
    Генерирует файл со случайными именами и фамилиями авторов
    
    Parameters:
    n: int - количество авторов
    """
    fake = Faker(['ru_RU'])

    with open('authors.txt', 'w') as file:
        for _ in range(n):
            file.write(fake.first_name() + ' ' + fake.last_name() + '\n')
    

if __name__ == '__main__':
    main()
