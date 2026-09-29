import time

menu = ''' \033[35m
Привет! 
Ты на главной странице приложения "MASH" 
Что ты можешь сделать:
1) Проверка знаний таблицы умножения;
2) Проверка сложения;
3) Проверка деления;
4) Выход из программы. \033[0m
'''

def check_result(answer, user_answer):
    try:
        if int(user_answer.strip()) == answer:
            print('\033[32mПравильно, ты супер!\n\033[0m')
            return 1
        else:
            print('\033[31mНеправильно, давай дальше...\n\033[0m')
            return 0
    except ValueError:
        print('\033[31mНеправильно, давай дальше...\n\n\033[0m')
        return 0
    

def multiply_test():
    result = 0
    a = input(
        '\033[36mСколько будет 2*2? \033[0m'
    )
    result+=check_result(4, a)

    a = input(
        '\033[36mСколько будет 2^3? \033[0m'
    )
    result+=check_result(8, a)
    a = input(
        '\033[36mСколько будет 6*6? \033[0m'
    )
    result+=check_result(36, a)
    a = input(
        '\033[36mСколько будет 4*7? \033[0m'
    )
    result+=check_result(28, a)
    a = input(
        '\033[36mСколько будет 9*1? \033[0m'
    )
    result+=check_result(9, a)
    a = input(
        '\033[36mСколько будет 5*6? \033[0m'
    )
    result+=check_result(30, a)
    print(f'\033[33mПоздравляем! Вы прошли тест и набрали {result} баллов!\033[0m\n\n\n')
    print('Возвращаем в главное меню...\n')
    time.sleep(4)
    print(menu)
    
    
def additive_test():
    result = 0
    a = input(
        '\033[36mСколько будет 2+2? \033[0m'
    )
    result+=check_result(4, a)

    a = input(
        '\033[36mСколько будет 10+5? \033[0m'
    )
    result+=check_result(15, a)
    a = input(
        '\033[36mСколько будет 5+7? \033[0m'
    )
    result+=check_result(12, a)
    a = input(
        '\033[36mСколько будет 5+4? \033[0m'
    )
    result+=check_result(9, a)
    a = input(
        '\033[36mСколько будет 20+15? \033[0m'
    )
    result+=check_result(35, a)
    a = input(
        '\033[36mСколько будет 149+245? \033[0m'
    )
    result+=check_result(394, a)
    print(f'Поздравляем! Вы прошли тест и набрали {result} баллов!\n')
    print('Возвращаем в главное меню...\n')
    time.sleep(4)
    print(menu)
    
    
def division_test():
    result = 0
    a = input(
        '\033[36mСколько будет 2/2? \033[0m'
    )
    result+=check_result(1, a)

    a = input(
        '\033[36mСколько будет 10/5? \033[0m'
    )
    result+=check_result(2, a)
    a = input(
        '\033[36mСколько будет 10/2? \033[0m'
    )
    result+=check_result(5, a)
    a = input(
        '\033[36mСколько будет 20/5? \033[0m'
    )
    result+=check_result(10, a)
    a = input(
        '\033[36mСколько будет 18/3? \033[0m'
    )
    result+=check_result(6, a)
    a = input(
        '\033[36mСколько будет 40/4? \033[0m'
    )
    result+=check_result(10, a)
    print(f'Поздравляем! Вы прошли тест и набрали {result} баллов!\n')
    print('Возвращаем в главное меню...\n')
    time.sleep(4)
    print(menu)
    

def main():
    k=0
    while True:
        if k==0:
            print(menu)
        a=input('Введи цифру от 1 до 4 чтобы выбрать пункт: ')
        k+=1

        try:
            if int(a.strip()) == 1:
                multiply_test()
            elif int(a.strip()) == 2:
                additive_test()
            elif int(a.strip()) == 3:
                division_test()
            elif int(a.strip()) == 4:
                print('Ты вышел!')
                break
            else:
                print('Неправильные цифры, попробуй снова!')
        except ValueError:
            print('Ты ввел не число')


main()
