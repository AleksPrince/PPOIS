# fifteen/ui.py

from fifteen.board import Board

def print_menu():
    print("\nМеню:")
    print("1. Показать поле")
    print("2. Сделать ход (вверх/вниз/влево/вправо)")
    print("3. Проверить, решена ли головоломка")
    print("4. Выход")

def main():
    board = Board()
    print("Добро пожаловать в игру 'Пятнашки'!")

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == '1':
            print("\nТекущее поле:")
            print(board)

        elif choice == '2':
            direction = input("Введите направление (up/down/left/right): ").lower()
            if board.move(direction):
                print("Ход выполнен.")
            else:
                print("Невозможно выполнить ход в этом направлении.")

        elif choice == '3':
            if board.is_solved():
                print("Поздравляем! Головоломка решена.")
            else:
                print("Головоломка ещё не решена.")

        elif choice == '4':
            print("Выход из игры.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()
