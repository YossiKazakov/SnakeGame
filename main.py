# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import deque


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class A:
    def __init__(self):
        self.__x = 5

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x


# Press the green button in the gutter to run the script.

def sol(num, words):
    num = str(num)
    d = {"a": 2, "b": 2, "c": 2, "d": 3, "e": 3, "f": 3, "g": 4, "h": 4, "i": 4, "j": 5, "k": 5, "l": 5, "m": 6, "n": 6,
         "o": 6, "p": 7, "q": 7, "r": 7, "s": 7, "t": 8, "u": 8, "v": 8, "w": 9, "x": 9, "y": 9, "z": 9}
    for word in words:
        word_translation = ""
        for char in word:
            word_translation += str(d[char])
        if word_translation in num:
            print(word)


if __name__ == '__main__':
    # sol(3662277, ["foo", "bar", "baz", "foobar", "emo", "cat", "car", "cap"])
    w = ["foo", "bar", "baz", "foobar", "emo", "cat", "car", "cap"]
    # w = deque(w)
    s = 1
    print(s != None)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
