"""
    1. Реализовать класс JsonFileDriver, который будет описывать логику считывания (записи) элементов из (в) json файл.
    2. Реализовать класс SimpleFileDriver, который будет описывать логику считывания (записи) элементов из (в) файл.
    3. В блоке __main__ протестировать работу драйверов
"""
import json
import os
import pickle
from typing import Sequence
from abc import ABC, abstractmethod


class IStructureDriver(ABC):
    @abstractmethod
    def read(self) -> Sequence:
        """
        Считывает информацию из драйвера и возвращает её для объекта, использующего этот драйвер
        :return Последовательность элементов, считанная драйвером, для объекта
        """
        pass

    @abstractmethod
    def write(self, data: Sequence) -> None:
        """
        Получает информацию из объекта, использующего этот драйвер, и записывает её в драйвер
        :param data Последовательность элементов, полученная от объекта, для записи драйвером
        """
        pass


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename: str):
        self._filename = filename

    def read(self) -> Sequence:
        with open(self._filename) as file:
            return json.load(file)

    def write(self, data: Sequence) -> None:
        with open(self._filename, "w") as file:
            json.dump(data, file)


class PickleFileDriver(IStructureDriver):
    def __init__(self, filename):
        self._filename = filename

    def read(self) -> Sequence:
        with open(self._filename, "rb") as f:
            result = pickle.load(f)
            return result

    def write(self, data: Sequence) -> None:
        with open(self._filename, "wb") as f:
            pickle.dump(data, f)


#
# class SimpleFileDriver(IStructureDriver):
#     ...

if __name__ == '__main__':
    FILE = "/tmp/my_pickle"
    JFILE = "/tmp/my_json.json"

    a = {"a": "first", "b": "second", "c": "third", "d": ["a", "b", "c"],
         "a": "first", "b": "second", "c": "third", "d": ["a", "b", "c"],
         "a": "first", "b": "second", "c": "third", "d": ["a", "b", "c"],
         "a": "first", "b": "second", "c": "third", "d": ["a", "b", "c"],
         "x": "s"
         }

    new_my_driver = PickleFileDriver(FILE)
    new_my_driver.write(a)
    print("size of ", FILE, ": ", os.lstat(FILE).st_size)
    print(new_my_driver.read())

    new_my_driver = JsonFileDriver(JFILE)
    new_my_driver.write(a)
    print("size of ", JFILE, ": ", os.lstat(JFILE).st_size)
    print(new_my_driver.read())
