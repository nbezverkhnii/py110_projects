from typing import List, Set

def print_board(matrix: List[str]) -> None:
    """
    Выводит на экран игровое поле. Игровое поле - multi-line строка.
    В таком виде код легко масштабируется для поля любого размера больше 3
    
    d (dimension) - длина строки игрового поля
    
    row_list содержит строки матрицы (например, 3х3):
        [matrix[0:3], 
         matrix[3:7], 
         matrix[6:9]]
         
    [''] добавляется для праивльной отрисовки игравого поля в консоли
    Отдельные ячейки отделяются друг от друга симоволм "|"
    
    Parameters
    ----------
    matrix: List[str]
        Список, заполненный "X" или "О", или " "
    """
    d = 3
    
    row_list = [matrix[i*d:(i+1)*d] for i in range(d)] #row_list[0] = [' ', ' ', ' ']
    row_list = list(map(lambda x: [''] + x + [''], row_list)) #row_list[0] = ['', ' ', ' ', ' ', '']
    
    board = ''
    for row in reversed(row_list):
        board += '|'.join(row) + '\n'
 
    print('\n' + board)

    
def input_value(user: str, last_input: Set[str]) -> int:
    """
    Пользовательский ввод.
    
    Выполняется проверка введенного пользователем числа:
    - точно ли пользователь ввел число, а не букву
    - лежит ли введенное пользователем число в диапазоне 1-9 (для игры 3х3)
    - не ввел ли пользователь позицию, которая была занята ранее
    
    Если все проверки прошли прошли успешно, то число приводится к типу int.
    cheak_list преобразован к типу set, чтобы быстрее осуществлять поиск элементов
    
    Parameters
    ----------
    user: str 
        Текущий пользователь Х или О
    last_input: Set[str]
        Список введенных ранее значений
        
    Returns
    -------
    number: int
        Число 1-9, введенное пользователем.
    
    """
    number = input(f'Пользователь {user}, введите число ')
    cheak_list = set([str(i) for i in range(1, 10)]) # {'1','2',...} 
    
    
    def is_digit(number):
        return not number.isdigit()
   

    def ch_list(number):
        return not number in cheak_list
    
    
    def is_last(number):
        return int(number) in last_input
    
    while is_digit(number) or ch_list(number) or is_last(number):
        number = input('Вы ввели что-то не то. \nВведите снова: ')
        
    return int(number)


def cheak_win(user: str, board_matrix: List[str], step: int) -> bool:
    """
    Проверка победы.

    Выполняется проверка условий победы для строк, столбцов и диагоналей игрового поля.
    Выиграть можно не раньше, чем на 5 ходу, поэтому if step > 4

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
    win_combination = [user]*3 #['X', 'X', 'X'] или ['O', 'O', 'O']  
    win_case_list = []
    
    for i in range(3):
        win_case_list.append(board_matrix[i*3:(i+1)*3] == win_combination) # строки
        win_case_list.append(board_matrix[i:9:3] == win_combination) # столбцы
        
    win_case_list.append(board_matrix[0:9:4] == win_combination) # диагонали
    win_case_list.append(board_matrix[2:7:2] == win_combination) # диагонали
        
    if step > 4 and any(win_case_list):
        print('\n' + f'Пользователь {user} выиграл!!!' + '\n')
        result = True
    else:
        result = False
    
    return result

    
def cheak_pass(step: int, win: bool) -> None:
    """
    Проверка на ничью.

    Parameters
    ----------
    step: int
        Номер игрового хода
    win: bool
        Была ли победа на последнем ходу 
    """
    if step == 9 and not win:
        print('Ничья!' + '\n')


def next_game() -> bool:
    """
    Функция спрашивает разрешение на следущую игру.
    
    Returns
    -------
    bool
        Если играем еще - True, если нет - False
    """
    
    result = input('\n' + 'Хотите попробовать еще? Да[д]\Нет[что-угодно]: ')
    
    if result == 'д':
        return True
    else:
        return False
    
    
def tic() -> None:
    """
    Реализаует логику по правилам игры в "Крестики-Нолики".
    
    Инициализируются слудующие перменные:
        board_matrix - отображение 2D-матрицы в 1D. 3х3=9 элементов. 
        step -  номер игрового хода
        last_input - содержит занятые ячейки на игровом поле
        user_item - "тумблер" переключения игроков.
        user -  выступает одновременно и как "имя" игрока, и как символ, 
        которм заполняется выбранное играком поле
    """
    
    board_matrix = [' ' for _ in range(9)]
    step = 0
    last_input = set()
    user_item = {'X':'O', 'O':'X'}
    
    # Первый ходит Х
    user = user_item['O'] # user = 'X'
    win = False

    while step < 9 and not win:
        
        # Ход пользователя
        user_1_input = input_value(user, last_input)
        
        last_input.add(user_1_input)
        board_matrix[user_1_input-1] = user
        print_board(board_matrix)
        step += 1
        
        # Проверка на выигрыш и ничью
        win = cheak_win(user, board_matrix, step)
        cheak_pass(step, win)
        
        #Смена пользователя
        user = user_item[user] # user_item['X'] = 'O'

        
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
    
