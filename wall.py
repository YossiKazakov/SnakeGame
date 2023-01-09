from constants import *
from game_utils import get_random_wall_data


class Wall:
    color = "blue"

    def __init__(self):
        self.__x, self.__y, self.__direction = get_random_wall_data()
        self.__coordinates = self.generate_coordinates()

    def generate_coordinates(self):
        if self.__direction == LEFT or self.__direction == RIGHT:
            return [(self.__x - 1, self.__y), (self.__x, self.__y), (self.__x + 1, self.__y)]
        if self.__direction == UP or self.__direction == DOWN:
            return [(self.__x, self.__y - 1), (self.__x, self.__y), (self.__x, self.__y + 1)]

    def movement_logic(self):
        if self.__direction == UP:
            for i, cell in enumerate(self.__coordinates):
                self.__coordinates[i] = cell[0], cell[1] + 1
        if self.__direction == DOWN:
            for i, cell in enumerate(self.__coordinates):
                self.__coordinates[i] = cell[0], cell[1] - 1
        if self.__direction == LEFT:
            for i, cell in enumerate(self.__coordinates):
                self.__coordinates[i] = cell[0] - 1, cell[1]
        if self.__direction == RIGHT:
            for i, cell in enumerate(self.__coordinates):
                self.__coordinates[i] = cell[0] + 1, cell[1]

    @property
    def coordinates(self):
        return self.__coordinates
