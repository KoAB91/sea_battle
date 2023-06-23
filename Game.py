import sys

from Player import *
from random import randint
from MyExceptions import *


class Game:

    user = None
    ai = None
    user_board = None
    ai_board = None

    def random_ship(self, board: Board, length: int):
        counter = 0
        while True:
            if counter <= 2000:
                try:
                    board.add_ship(length, Dot(randint(1, 6), randint(1, 6)), randint(0, 1))
                    break
                except ShipCreatingException:
                    counter += 1
                    continue
            else:
                raise ShipCreatingException('Слишком много попыток')

    def random_board(self, hide=True):
        player_board = None
        while True:
            try:
                player_board = Board(hide)
                self.random_ship(player_board, 3)
                self.random_ship(player_board, 2)
                self.random_ship(player_board, 2)
                self.random_ship(player_board, 1)
                self.random_ship(player_board, 1)
                self.random_ship(player_board, 1)
                self.random_ship(player_board, 1)
                break
            except ShipCreatingException:
                continue

        return player_board

    def create_ship(self, type: str, player_board: Board, length: int):
        print('-' * 24, f'Разместим {type} корабль.', sep='\n')
        player_board.show()
        x, y, direct = None, None, None
        while True:
            try:
                x, y = [int(x) for x in input('Введите координаты клетки, '
                                              'в которой будет распологаться нос корабля: ').split()]
            except Exception:
                print('Необходимо ввести целые числа в диапозоне от 1 до 6 через пробел!')
                continue

            head = Dot(x, y)
            if player_board.out(head):
                print('Клетка находится за пределами поля!')
                continue

            if length > 1:
                try:
                    direct = int(input('Укажите направление корабля, где 1 - горизонтальное, 0 - вертикальное: '))
                except Exception:
                    print('Необходимо указать целое числа 0 или 1!')
                    continue

            try:
                player_board.add_ship(length, Dot(x, y), direct)
            except ShipCreatingException as e:
                print(e)
                continue
            else:
                break

    def create_board(self):
        player_board = Board(False)
        self.create_ship('трехпалубный', player_board, 3)
        self.create_ship('двухпалубный', player_board, 2)
        self.create_ship('двухпалубный', player_board, 2)
        for i in range(4):
            self.create_ship('однопалубный', player_board, 1)

        return player_board

    def greet(self):
        print('Добро пожаловать в игру.....')
        print('<' * 12, 'Морской бой!', '>' * 12)
        print('-' * 24)
        print('Правила игры:', '1. Цель игры - потопить все вражеские корабли.',
              '2. На старте игры Вы размещаете 7 своих кораблей (1 - трехпалубный, 2 - двухпалубных, 4 - однопалубных)'
              'на поле таким образом,\nчтобы они не пересекались и между ними находилась хотя бы одна свободная клетка.'
              ' Для размещения корабля необходимо будет\nввести координаты клетки, в которой будет распологаться'
              'нос корабля, а, далее, как он будет распологаться - горизонтально или вертикально.',
              '3. Далее, поочередно с соперником производите выстрелы в попытке потопить вражеский корабль.\n'
              'Выстрелы осуществляются посредством ввода координат клетки в формате "x y", '
              'где x - координата клетки по горизонтали, а y - по вертикали. Если выстрел был точным, '
              'игрок ходит еще раз.', sep='\n')

        print('-' * 24, '-' * 24, sep='\n')
        answer = input('Готовы начать? [y/n]: ')
        if answer != 'y':
            print('-' * 24, '-' * 24, sep='\n')
            print('Обязательно возвращайтесь скорее! До встречи в новом бою!')
            sys.exit()

    def loop(self):
        answer = input('Вы хотите самостоятельно разместить Ваши корабли? [y/n]: ')
        if answer == 'y':
            user_board = self.create_board()
        else:
            user_board = self.random_board(False)
            print('Расположение Ваших кораблей: ')
            user_board.show()

        ai_board = self.random_board()
        answer = input('Вы хотите включить режим подсветки контура потопленных кораблей? [y/n]: ')
        if answer == 'y':
            ai_board.set_easy_mode(True)

        user = User(user_board, ai_board)
        ai = AI(ai_board, user_board)

        while True:
            winner = self.player_turn(user)
            if winner:
                break
            winner = self.player_turn(ai)
            if winner:
                break

        print('-' * 24, '-' * 24, sep='\n')
        print(f'Победил {winner}!')
        print('Спасибо за игру! Обязательно возвращайтесь скорее! До встречи в новом бою!')

    def player_turn(self, player: Player):
        player_name = 'игрок' if isinstance(player, User) else 'ИИ'
        print('=' * 24, f'Ходит {player_name}', '=' * 24, sep='\n')
        while True:
            if player_name == 'игрок':
                print('Кораблей противника осталось:')
                player.get_enemy_board().show_ships_remainder()
                print('Ваших кораблей осталось:')
                player.get_player_board().show_ships_remainder()
                player.get_enemy_board().show()

            try:
                good_shot = player.move()
            except BoardOutException as e:
                if player_name == 'игрок':
                    print(e)
                continue
            if player_name == 'ИИ':
                player.get_enemy_board().show()
            if good_shot:
                if player.get_enemy_board().get_living_ships() == 0:
                    print('-' * 24)
                    player.get_enemy_board().show()
                    return player_name
                continue

            return None

    def start(self):
        self.greet()
        self.loop()
