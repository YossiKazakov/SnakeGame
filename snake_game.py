from typing import Optional
from game_display import GameDisplay
from snake import *
from wall import *
from apple import *
from constants import *


class SnakeGame:

    def __init__(self, width: int, height: int, max_apples: int, max_walls: int, rounds: int) -> None:
        self.__width = width
        self.__height = height
        self.__rounds = rounds if rounds > -1 else float("inf")
        self.__current_round = 0
        self.__score = 0
        self.__max_apples = max_apples
        self.__max_walls = max_walls
        self.__occupied_cells = set()

        self.__snake = Snake(width, height)
        self.__apples = set()
        self.__walls = set()

        self.__key_clicked = UP

        self.add_wall()
        self.add_apple()

        self.update_occupied_cells()

    """ ****************** Getters and Setters ****************** """

    @property
    def rounds(self) -> int:
        return self.__rounds

    @rounds.setter
    def rounds(self, updated_num_of_rounds) -> None:
        self.__rounds = updated_num_of_rounds

    @property
    def score(self) -> int:
        return self.__score

    """ ********************** Validations ********************** """

    def head_is_in_board(self) -> bool:
        head_x, head_y = self.__snake.head
        return 0 <= head_x < self.__width and 0 <= head_y < self.__height

    def head_is_not_in_body(self) -> bool:
        return self.__snake.snake_coordinates.count(self.__snake.head) == 1

    def coordinate_in_bounds(self, x, y) -> bool:
        return 0 <= x < self.__width and 0 <= y < self.__height

    """ ************* Adding and maintaining objects ************ """

    def add_apple(self) -> None:
        if len(self.__apples) < self.__max_apples:
            apple = Apple()
            while apple.cell in self.__occupied_cells:
                apple = Apple()
            self.__apples.add(apple)

    def add_wall(self) -> None:
        if len(self.__walls) < self.__max_walls:
            wall = Wall()
            while set(wall.coordinates) & self.__occupied_cells:
                wall = Wall()
            self.__walls.add(wall)

    def create_new_walls_logic(self) -> None:
        walls_to_remove = set()
        for wall in self.__walls:
            if not any(self.coordinate_in_bounds(*wall_coordinate) for wall_coordinate in wall.coordinates):
                walls_to_remove.add(wall)
        self.__walls -= walls_to_remove

    def update_occupied_cells(self) -> None:
        self.__occupied_cells.clear()
        for cell in self.__snake.snake_coordinates:
            self.__occupied_cells.add(cell)
        for apple in self.__apples:
            self.__occupied_cells.add(apple.cell)
        for wall in self.__walls:
            for wall_cell in wall.coordinates:
                self.__occupied_cells.add(wall_cell)

    """ ****************** Objects interaction ****************** """

    def snake_eating_apple_logic(self) -> int:
        for apple in self.__apples:
            if self.__snake.head == apple.cell:
                self.__apples.remove(apple)
                self.__snake.rounds_of_lengthening += 3
                return self.__snake.points_when_eating
        return 0

    def wall_hit_an_apple(self) -> None:
        apples_to_remove = set()
        for wall in self.__walls:
            for apple in self.__apples:
                if apple.cell in wall.coordinates:
                    apples_to_remove.add(apple)
        self.__apples -= apples_to_remove

    def wall_hit_the_snake(self) -> bool:
        """
        :return: True or False whether to continue or end the game
        """
        # first check if head hit a wall, if so, return True so that self.is_over will also return True
        for wall in self.__walls:
            if self.__snake.head in wall.coordinates:
                return True
        # find the index of the closest cell to head that was hit
        closest_cell_to_head = -1
        for coordinate in self.__snake.snake_coordinates:
            for wall in self.__walls:
                if coordinate in wall.coordinates:
                    closest_cell_to_head = max(self.__snake.snake_coordinates.index(coordinate), closest_cell_to_head)
        self.__snake.snake_coordinates = deque(list(self.__snake.snake_coordinates)[closest_cell_to_head + 1:])
        # if only the head was left end the game return True so that self.is_over will also return True
        if len(self.__snake.snake_coordinates) == 1:
            return True
        # else, if the snake was only cut (or not even touched) the game should continue so return False
        return False

    """ ***************** Each round game logic ***************** """

    def read_key(self, key_clicked: Optional[str]) -> None:
        if key_clicked == "Up":
            self.__key_clicked = UP
        if key_clicked == "Down":
            self.__key_clicked = DOWN
        if key_clicked == "Left":
            self.__key_clicked = LEFT
        if key_clicked == "Right":
            self.__key_clicked = RIGHT

    def update_objects(self) -> None:
        # Update snake
        self.__snake.movement_logic(self.__key_clicked)
        self.update_occupied_cells()

        # Update walls
        if self.__current_round % 2 == 0:
            for wall in self.__walls:
                wall.movement_logic()
        self.create_new_walls_logic()
        self.add_wall()
        self.update_occupied_cells()

        # Update apples
        self.add_apple()
        self.update_occupied_cells()

        # Check if snake ate apple
        add_to_score = self.snake_eating_apple_logic()

        # Check if wall hit an apple
        self.wall_hit_an_apple()

        # Update size and points accordingly
        self.__snake.update_points_according_to_size()

        # Update score
        self.__score += add_to_score

        # Update rounds
        self.__current_round += 1

    def draw_board(self, gd: GameDisplay) -> None:
        # Draw snake
        for x, y in self.__snake.snake_coordinates:
            if self.coordinate_in_bounds(x, y):
                gd.draw_cell(x, y, Snake.color)

        # Draw apples
        for apple in self.__apples:
            x, y = apple.cell
            gd.draw_cell(x, y, Apple.color)

        # Draw walls
        for wall in self.__walls:
            for x, y in wall.coordinates:
                if self.coordinate_in_bounds(x, y):
                    gd.draw_cell(x, y, Wall.color)

    def end_round(self) -> None:
        pass

    def is_over(self) -> bool:
        return not (self.head_is_in_board() and self.head_is_not_in_body()) \
               or self.__current_round == self.rounds + 1 or self.wall_hit_the_snake()
