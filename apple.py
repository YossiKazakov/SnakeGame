from game_utils import get_random_apple_data


class Apple:
    color = "green"

    def __init__(self):
        self.__x, self.__y = get_random_apple_data()

    @property
    def cell(self):
        return self.__x, self.__y
