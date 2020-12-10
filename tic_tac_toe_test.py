from typing import List, Set

# Размер поля игры в Крестики-Нолики 3х3
SIZE = 3

def print_board(matrix: List[str]) -> None:
    """
    Выводит на экран игровое поле. Игровое поле - multi-line строка.
    В таком виде код легко масштабируется для поля любого размера больше 3
       
    row_list содержит строки матрицы (например, 3х3):
        [matrix[0:3], 
         matrix[3:7], 
         matrix[6:9]]
         
    Отдельные ячейки при отрисовке отделяются друг от друга симоволм "|"
    
    Parameters
    ----------
    matrix: List[str]
        Список, заполненный "X" или "О", или " "

    >>> print_board(['', ' ', ' ', ' ', '','', ' ', ' ', ' ', '','', ' ', ' ', ' ', ''])
    >>> | | | |
        | | | |
        | | | |
    """
    
    row_list = [matrix[i*SIZE:(i+1)*SIZE] for i in range(SIZE)] #row_list[0] = [' ', ' ', ' ']

    # [''] добавляется для праивльной отрисовки игравого поля в консоли
    row_list = list(map(lambda x: [''] + x + [''], row_list)) 
    
    board = ''
    # reversed - чтобы строка с номерами ячеек 1,2,3 оказалсь внизу
    for row in reversed(row_list):
        board += '|'.join(row) + '\n'
 
    print('\n' + board)

    
def input_value(user: str, last_input: Set[str]) -> int:
    """
    Пользовательский ввод.
    
    Выполняется проверка введенного пользователем числа:
    - точно ли пользователь ввел число, а не букву
    - лежит ли введенное пользователем число в диапазоне 1-9 (для игры 3х3)
    (допустимые значения для ввода содержатся в cheak_list)
    - не ввел ли пользователь позицию, которая была занята ранее
    
    Если все проверки прошли прошли успешно, то число приводится к типу int.
    
    Parameters
    ----------
    user: str 
        Текущий пользователь Х или О
    last_input: Set[str]
        Список введенных ранее значений
        
    Returns
    -------
    number: int
        Число, введенное пользователем.
    
    """    
    number = input(f'Пользователь {user}, введите число ')
    # x*x быстрее, чем x**2
    # преобразован к типу set, чтобы быстрее осуществлять поиск элементов
    cheak_list = set([str(i) for i in range(1,SIZE*SIZE+1)])
    
    
    def is_not_digit(number):
        return not number.isdigit()
   

    def not_in_chack_list(number):
        return not number in cheak_list
    
    
    def in_last_input(number):
        return int(number) in last_input
    
    while is_not_digit(number) or not_in_chack_list(number) or in_last_input(number):
        number = input('Вы ввели что-то не то. \nВведите снова: ')
        
    return int(number)


def cheak_win(user: str, board_matrix: List[str], step: int) -> bool:
    """
    Проверка победы.

    Выполняется проверка условий победы для строк, столбцов и диагоналей игрового поля.
    
    Parameters
    ----------
    user: str
        Игрок данного хода
    board_matrix:  list
        Матрица со значениями игрового поля
    step: int
        Номер игрового хода

    Returns
    -------
    bool
        Если победа - True, если нет - False.

    """   
    # Победа - кобимнация одинаковых символов длиной SIZE
    win_combination = [user]*SIZE #['X', 'X', 'X'] 
    win_case_list = []
    
    for i in range(SIZE):
        win_case_list.append(board_matrix[i*SIZE:(i+1)*SIZE] == win_combination) # строки
        win_case_list.append(board_matrix[i:SIZE*SIZE:SIZE] == win_combination) # столбцы
    
    # У двумерной матрицы две диагонали
    main_diagonal = board_matrix[0:SIZE*SIZE:SIZE+1] == win_combination
    antidiagonal = board_matrix[SIZE-1:SIZE*SIZE-2:SIZE-1] == win_combination   
    win_case_list.append(main_diagonal)
    win_case_list.append(antidiagonal)
    
    result = False
    # Выиграть можно не раньше, чем сделано SIZE+1 ходов    
    if step > SIZE+1 and any(win_case_list):
        print('\n' + f'Пользователь {user} выиграл!!!' + '\n')
        result = True
    
    return result

    
def cheak_pass(step: int, win: bool) -> None:
    """
    Проверка на ничью.
    Ничья ничья наступает, когда ходы уже закончились, 
    а победа ни одного из пользователей не наступила

    Parameters
    ----------
    step: int
        Номер игрового хода
    win: bool
        Была ли победа на сделанном ходу 
    """
    if step == SIZE*SIZE and not win:
        print('Ничья!\n')


def next_game() -> bool:
    """
    Функция спрашивает разрешение на следущую игру.
    Просит пользователя ввести ответ на вопрос в консоль.
    
    Returns
    -------
    bool
        Если играем еще - True, если нет - False
    """
    result = input('\nХотите попробовать еще? Да[д]\Нет[что-угодно]: ')
    return True if result == 'д' else False
    
 
def tic() -> None:
    """
    Реализаует логику по правилам игры в "Крестики-Нолики".
    
    Инициализируются слудующие перменные:
    board_matrix - отображение 2D-матрицы в 1D. SIZE*SIZE элементов. 
    step -  номер игрового хода
    last_input - содержит занятые ячейки на игровом поле
    user_item - "тумблер" переключения игроков.
    user -  выступает одновременно и как "имя" игрока, и как символ, 
                          которм заполняется выбранное играком поле
    """
    board_matrix = [' ' for _ in range(SIZE*SIZE)]
    step = 0
    last_input = set()
    user_item = {'X':'O', 'O':'X'}
    
    # Первый ходит Х
    user = user_item['O'] # user = 'X'
    win = False
    
    # Всего SIZE*SIZE-1 ходов за игру 
    while step < SIZE*SIZE and not win:
        
        # Ход пользователя
        user_input = input_value(user, last_input)
        
        last_input.add(user_input)
        board_matrix[user_input-1] = user
        print_board(board_matrix)
        step += 1
        
        # Проверка на выигрыш и ничью
        win = cheak_win(user, board_matrix, step)
        cheak_pass(step, win)
        
        # Нужно сменить пользователя
        user = user_item[user]

        
def main() -> None:
    """
    Главная функция.
    
    Выводит на экран правила игры.
    Условие начала новой партии - согласие пользователя:
    suggestion = True.
    Об этом пользователя спрашивает функция next_game()
    Логика игры реализована в функции tic()
    """
    
    rules = """
    Это игра "Крестики-Нолики"
    Первыми ходят Х, вторыми О.
    Для ввода используете цифры от 1-9 на боковой панели клавиатуры.
    | | | |     |7|8|9|
    | | | | <-> |4|5|6|
    | | | |     |1|2|3|
    """
    print(rules)
    
    suggestion = True
    while suggestion:
        tic()
        suggestion = next_game()


if __name__ == '__main__':
    main()
    
