from constants import *
import math
from collections import deque


class Snake:
    color = "black"

    def __init__(self, max_x, max_y):
        self.__size = SNAKE_SIZE
        self.__direction = UP
        self.__head = (max_x // 2, max_y // 2)
        self.__snake_coordinates = deque(reversed([(self.__head[0], self.__head[1] - i) for i in range(SNAKE_SIZE)]))
        self.__points_when_eating = int(math.sqrt(self.__size))
        self.__rounds_of_lengthening = 0

    def valid_direction(self, direction) -> bool:
        if self.__direction == UP and direction == DOWN:
            return False
        if self.__direction == DOWN and direction == UP:
            return False
        if self.__direction == RIGHT and direction == LEFT:
            return False
        if self.__direction == LEFT and direction == RIGHT:
            return False
        return True

    def movement_logic(self, direction):
        # if the direction given is opposite to current one, don't update the current one
        if self.valid_direction(direction):
            self.__direction = direction

        if self.__direction == UP:
            self.__head = self.__head[0], self.__head[1] + 1
        if self.__direction == DOWN:
            self.__head = self.__head[0], self.__head[1] - 1
        if self.__direction == LEFT:
            self.__head = self.__head[0] - 1, self.__head[1]
        if self.__direction == RIGHT:
            self.__head = self.__head[0] + 1, self.__head[1]

        # Pop from back, append to new head to front or just append new head if lengthening
        self.lengthening()

    def lengthening(self):
        if self.__rounds_of_lengthening == 0:
            self.__snake_coordinates.popleft()
            self.__snake_coordinates.append(self.__head)
        else:
            self.__snake_coordinates.append(self.__head)
            self.__rounds_of_lengthening -= 1

    def update_points_according_to_size(self):
        self.__size = len(self.__snake_coordinates)
        self.__points_when_eating = int(math.sqrt(self.__size))

    @property
    def snake_coordinates(self):
        return self.__snake_coordinates

    @snake_coordinates.setter
    def snake_coordinates(self, new_deque):
        self.__snake_coordinates = new_deque

    @property
    def points_when_eating(self):
        return self.__points_when_eating

    @property
    def head(self):
        return self.__head

    @property
    def direction(self):
        return self.__direction

    @property
    def rounds_of_lengthening(self):
        return self.__rounds_of_lengthening

    @rounds_of_lengthening.setter
    def rounds_of_lengthening(self, new_num_of_rounds):
        self.__rounds_of_lengthening = new_num_of_rounds

