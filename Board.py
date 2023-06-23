from Ship import Ship
from Dot import Dot
from MyExceptions import *


class Board:

    def __init__(self, hide: bool):
        self.field = [[' '] * 6 for i in range(6)]
        self.ships = []
        self.hide = hide
        self.living_ships = 0
        self.occupied_dots = dict()
        self.easy_mode = False
        self.ships_type = {3: 0, 2: 0, 1: 0}

    def get_ships(self):
        return self.ships

    def get_living_ships(self):
        return self.living_ships

    def set_easy_mode(self, value):
        self.easy_mode = value

    def get_ships_type(self):
        return self.ships_type

    def get_occupied_dots(self):
        return self.occupied_dots

    def out(self, dot: Dot):
        if not 1 <= dot.get_x() <= 6 or not 1 <= dot.get_y() <= 6:
            return True
        return False

    def add_ship(self, length: int, head: Dot, direction: int):

        if length > 1:
            if direction and head.get_y() + length - 1 > 6:
                raise ShipCreatingException('Корабль выходит за границы поля')

            if not direction and head.get_x() + length - 1 > 6:
                raise ShipCreatingException('Корабль выходит за границы поля')

        nw_ship = Ship(length, head, direction)
        for dot in nw_ship.get_dots():
            for ship in self.ships:
                if dot in ship.get_dots():
                    raise ShipCreatingException('Корабли пересекаются')
            for ship_counter in self.occupied_dots.values():
                if dot in list(ship_counter):
                    raise ShipCreatingException('Расстояние между кораблями должно быть минимум 1 клетка')

        self.ships.append(nw_ship)
        self.living_ships += 1
        self.ships_type[length] += 1
        nw_counter = self.counter(nw_ship)
        self.occupied_dots[id(nw_ship)] = nw_counter

        if not self.hide:
            for dot in nw_ship.get_dots():
                self.field[dot.get_x() - 1][dot.get_y() - 1] = '■'

    def counter(self, ship: Ship) -> list:
        counter_dots = []
        x = ship.get_head().get_x()
        y = ship.get_head().get_y()
        direction = ship.get_direction()

        # первый ряд
        if x == 1:
            if direction:
                if y != 1:
                    counter_dots.append(Dot(x, y - 1))
                    counter_dots.append(Dot(x + 1, y - 1))
                for dot in ship.get_dots():
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                dot = ship.get_dots()[-1]
                if dot.get_y() < 6:
                    counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() + 1))
                return counter_dots
            else:
                if y != 1 and y != 6:
                    for dot in ship.get_dots():
                        counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                        counter_dots.append(Dot(dot.get_x(), dot.get_y() - 1))
                    dot = ship.get_dots()[-1]
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() - 1))
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() + 1))
                    return counter_dots

        # последний ряд
        if x == 6 and direction:
            if y != 1:
                counter_dots.append(Dot(x, y - 1))
                counter_dots.append(Dot(x - 1, y - 1))
            for dot in ship.get_dots():
                counter_dots.append(Dot(dot.get_x() - 1, dot.get_y()))
            dot = ship.get_dots()[-1]
            if dot.get_y() < 6:
                counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                counter_dots.append(Dot(dot.get_x() - 1, dot.get_y() + 1))
            return counter_dots

        # первый столбец
        if y == 1:
            if not direction:
                if x != 1:
                    counter_dots.append(Dot(x - 1, y))
                    counter_dots.append(Dot(x - 1, y + 1))
                for dot in ship.get_dots():
                    counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                dot = ship.get_dots()[-1]
                if dot.get_x() < 6:
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() + 1))
                return counter_dots
            else:
                for dot in ship.get_dots():
                    counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                    counter_dots.append(Dot(dot.get_x() - 1, dot.get_y()))
                dot = ship.get_dots()[-1]
                counter_dots.append(Dot(dot.get_x() - 1, dot.get_y() + 1))
                counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() + 1))
                return counter_dots

        # последний столбец
        if y == 6 and not direction:
            if x != 1:
                counter_dots.append(Dot(x - 1, y))
                counter_dots.append(Dot(x - 1, y - 1))
            for dot in ship.get_dots():
                counter_dots.append(Dot(dot.get_x(), dot.get_y() - 1))
            dot = ship.get_dots()[-1]
            if dot.get_x() < 6:
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() - 1))
            return counter_dots

        counter_dots.append(Dot(x, y - 1))
        counter_dots.append(Dot(x - 1, y - 1))
        counter_dots.append(Dot(x - 1, y))

        if direction:
            counter_dots.append(Dot(x + 1, y - 1))
            counter_dots.append(Dot(x + 1, y))
            for dot in ship.get_dots()[1:]:
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                counter_dots.append(Dot(dot.get_x() - 1, dot.get_y()))
            dot = ship.get_dots()[-1]
            if dot.get_y() < 6:
                counter_dots.append(Dot(dot.get_x() - 1, dot.get_y() + 1))
                counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() + 1))
        else:
            counter_dots.append(Dot(x - 1, y + 1))
            counter_dots.append(Dot(x, y + 1))
            for dot in ship.get_dots()[1:]:
                counter_dots.append(Dot(dot.get_x(), dot.get_y() + 1))
                counter_dots.append(Dot(dot.get_x(), dot.get_y() - 1))
            dot = ship.get_dots()[-1]
            if dot.get_x() < 6:
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() - 1))
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y()))
                counter_dots.append(Dot(dot.get_x() + 1, dot.get_y() + 1))

        return counter_dots

    def shot(self, shot: Dot) -> bool:
        if self.out(shot):
            raise BoardOutException('Координаты выстрела за пределами поля!')

        if self.field[shot.get_x() - 1][shot.get_y() - 1] == 'T' \
                or self.field[shot.get_x() - 1][shot.get_y() - 1] == 'X':
            raise BoardOutException('Вы уже делали выстрел по этим координатам!')

        for ship in self.ships:
            if shot in ship.get_dots():
                ship_lives = ship.get_lives()
                ship.set_lives(ship_lives - 1)
                if ship.get_lives() > 0:
                    print('>' * 10, 'Подбил!')
                else:
                    print('>' * 10, 'Потопил!')
                    self.living_ships -= 1
                    self.ships_type[ship.get_length()] -= 1
                    if self.easy_mode:
                        self.add_ship_counter(ship)
                self.field[shot.get_x() - 1][shot.get_y() - 1] = 'X'
                return True
        self.field[shot.get_x() - 1][shot.get_y() - 1] = 'T'
        print('>' * 10, 'Мимо!')
        return False

    def show(self):
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in range(6):
            print(f'{i + 1} |', ' | '.join(map(str, self.field[i])), '|')

    def add_ship_counter(self, ship: Ship):
        counter_dots = self.occupied_dots.get(id(ship))
        for dot in counter_dots:
            self.field[dot.get_x() - 1][dot.get_y() - 1] = '*'

    def show_ships_remainder(self):
        print(f'Трехпалубные - {self.ships_type[3]}; Двухпалубные - {self.ships_type[2]}; '
              f'Однопалубные - {self.ships_type[1]}')