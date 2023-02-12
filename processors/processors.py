from typing import Iterable
import abc

def cached_processor(Class):
    PROCESS_ATTR_NAME = 'process'
    LAST_RESULT_ATTR_NAME ='__cached_processor_last_result'
    LAST_TIMESTAMPS_ATTR_NAME ='__cached_processor_last_timestamps'

    process = getattr(Class, PROCESS_ATTR_NAME)

    def cached_process(self, timestamps, results):
        if timestamps == getattr(self, LAST_TIMESTAMPS_ATTR_NAME):
            return getattr(self, LAST_RESULT_ATTR_NAME)
        else:
            res = process(self, timestamps, results)
            setattr(self, LAST_TIMESTAMPS_ATTR_NAME, timestamps)
            setattr(self, LAST_RESULT_ATTR_NAME, res)
            return res

    setattr(Class, PROCESS_ATTR_NAME, cached_process)
    setattr(Class, LAST_RESULT_ATTR_NAME, None)
    setattr(Class, LAST_TIMESTAMPS_ATTR_NAME, None)
    return Class


class Processor(abc.ABC):
    def __init__(self, *sources: Iterable[object]):
        self.__sources = sources

    @abc.abstractmethod
    def process(self, source_timestamps, source_results):
        pass

    def __next__(self):
        # Process sources and "unzip" timestamps and results in two different lists
        timestamps, results = tuple(zip(*[next(source) for source in self.__sources]))
        return self.process(timestamps, results)
    
    def __iter__(self):
        return self