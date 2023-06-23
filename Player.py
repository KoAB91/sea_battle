from Board import Board
from Dot import Dot
from random import randint


class Player:

    player_board = None
    enemy_board = None

    def __init__(self, player_board: Board, enemy_board: Board):
        self.player_board = player_board
        self.enemy_board = enemy_board

    def ask(self) -> Dot:
        pass

    def move(self):
        dot = self.ask()
        return self.enemy_board.shot(dot)

    def get_enemy_board(self):
        return self.enemy_board

    def get_player_board(self):
        return self.player_board


class AI(Player):

    not_shoot_area = []

    def ask(self) -> Dot:
        enemy_ships = self.enemy_board.get_ships()
        enemy_counter_ships = self.enemy_board.get_occupied_dots()
        for ship in enemy_ships:
            if ship.get_lives() == 0:
                self.not_shoot_area += enemy_counter_ships[id(ship)]
        for ship in enemy_ships:
            if ship.get_lives() != 0 and ship.get_lives() < ship.get_length():

                min_x, max_x = 6, 1
                min_y, max_y = 6, 1
                for dot in ship.get_dots():
                    dot_x = dot.get_x()
                    dot_y = dot.get_y()
                    min_x = dot_x if min_x > dot_x else min_x
                    max_x = dot_x if max_x < dot_x else max_x
                    min_y = dot_y if min_y > dot_y else min_y
                    max_y = dot_y if max_y < dot_y else max_y

                min_x = min_x - 1 if min_x > 1 else min_x
                max_x = max_x + 1 if max_x < 6 else max_x
                min_y = min_y - 1 if min_y > 1 else min_y
                max_y = max_y + 1 if max_y < 6 else max_y

                x = randint(min_x, max_x)
                y = randint(min_y, max_y)
                return Dot(x, y)

        while True:
            x = randint(1, 6)
            y = randint(1, 6)
            dot = Dot(x, y)
            if dot not in self.not_shoot_area:
                break
        return Dot(x, y)


class User(Player):

    def ask(self) -> Dot:
        dot = None
        while True:
            try:
                x, y = [int(x) for x in input('Введите координаты выстрела: ').split()]
            except Exception:
                print('Необходимо ввести целые числа в диапозоне от 1 до 6 через пробел!')
                continue
            dot = Dot(x, y)
            if self.player_board.out(dot):
                print('Координаты должны находится в диапозоне от 1 до 6!')
                continue
            break
        return dot
