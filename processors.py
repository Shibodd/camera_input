from typing import Iterable, Callable
import abc

class CachedProcessor(abc.ABC):
    def __init__(self, source: Iterable[object]):
        self.__source = source
        self.__last_result = None
        self.__last_ns = None

    @abc.abstractmethod
    def process(self, result):
        pass

    def __next__(self):
        ns, sourceResult = next(self.__source)
        if ns == self.__last_ns:
            return self.__last_result
        else:
            self.__last_ns = ns
            self.__last_result = (ns, self.process(sourceResult))
            return self.__last_result
    
    def __iter__(self):
        return self

    def get_last_result(self):
        return self.__last_result