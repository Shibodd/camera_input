from typing import Iterable
import abc
import numpy as np
import time

def cached_processor(Class):
    """ A decorator which wraps the process method of a Processor with a cached version. """

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
    """ The base class for all processors. Implements the generator pattern and defines the process method as abstract. """

    def __init__(self, *sources: Iterable[object]):
        self.__sources = sources

    @abc.abstractmethod
    def process(self, source_timestamps, source_results):
        """ The process method is called with the source values and their timestamps, in the same order as they are passed to __init__. \n
            It should return a tuple containing the timestamp of the result and the result itself."""
        pass

    def __next__(self):
        # Process sources and "unzip" timestamps and results in two different lists
        timestamps, results = tuple(zip(*[next(source) for source in self.__sources]))
        return self.process(timestamps, results)
    
    def __iter__(self):
        return self


@cached_processor
class ArmProcessor(Processor):
    """ A point source which calculates the point of an arm attached to the middle of two point sources. """

    def __init__(self, westPointSource, eastPointSource, armLength):
        super().__init__(westPointSource, eastPointSource)
        self.armLength = armLength

    def process(self, _, sourceResults):
        west, east = sourceResults
        if west is None or east is None:
            ans = None
        else:
            diff = (east - west)
            diff_hat = diff / np.linalg.norm(diff)

            mid = west + diff / 2
            arm_hat = np.array([diff_hat[1], -diff_hat[0]])
            ans = mid + (arm_hat * self.armLength)

        return (time.monotonic_ns(), ans)