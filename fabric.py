"""
Паттерн "Фабричный метод".
    1. Реализовать класс SimpleFileBuilder для построения драйвера SimpleFileDriver
    2. В блоке __main__ убедиться в построении драйверов JsonFileDriver и SimpleFileDriver
    3. В паттерне "Стратегия" использовать фабрику для получение драйверов в getter свойства driver.
        Getter должен возвращать драйвер, если его нет, то вызывать фабрику для получения драйвера.
"""

from abc import ABC, abstractmethod

from driver import IStructureDriver, JsonFileDriver, PickleFileDriver
from linkedlist import DoubleLinkedList


class DriverBuilder(ABC):
    @abstractmethod
    def build(self):
        pass


class JsonFileBuilder(DriverBuilder):
    DEFAULT_NAME = 'untitled.json'

    @classmethod
    def build(cls) -> IStructureDriver:
        filename = input('Введите название json файла(.json): ').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.json'):
            filename = f'{filename}.json'

        return JsonFileDriver(filename)


class PickleFileBuilder(DriverBuilder):
    DEFAULT_NAME = 'untitled.bin'

    @classmethod
    def build(cls) -> IStructureDriver:
        filename = input('Введите название файла(.bin): ').strip()
        filename = filename or cls.DEFAULT_NAME
        if not filename.endswith('.bin'):
            filename = f'{filename}.bin'

        return PickleFileDriver(filename)


class FabricDriverBuilder:
    DRIVER_BUILDER = {
        'json': JsonFileBuilder,
        'pickle': PickleFileBuilder
    }
    DEFAULT_DRIVER = 'json'

    @classmethod
    def get_driver(cls):
        driver_name = input("Введите название драйвера: ")
        driver_name = driver_name or cls.DEFAULT_DRIVER

        driver_builder = cls.DRIVER_BUILDER[driver_name]
        return driver_builder.build()


class LinkedListWithDriver(DoubleLinkedList):
    def __init__(self, drv=None):
        self._driver = drv
        super().__init__()

    @property
    def driver(self) -> IStructureDriver:
        if self._driver is None:
            self._driver = FabricDriverBuilder.get_driver()

        return self._driver

    def read(self):
        self.clear()
        for i in self._driver.read():
            self.append(i)

    def write(self):
        ls = [i for i in self]
        self._driver.write(ls)
