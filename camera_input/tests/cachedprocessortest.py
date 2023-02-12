import unittest
from processors.processors import Processor, cached_processor

@cached_processor
class TestProcessor(Processor):
    def process(self, source_timestamps, source_results):
        return (source_timestamps[0], source_results[0])


class CachedProcessorTest(unittest.TestCase):
    def test_does_not_cache(self):
        old_ts = -1

        proc = TestProcessor(((ts, ts + 1) for ts in range(3))) # Use a source that changes value every time, and value ts + 1
        for ts, res in proc:
            self.assertTrue(ts != old_ts and res == ts + 1) # Expect to always have new values
            old_ts = ts

    def test_does_cache(self):
        START_VAL = 0

        # Use a source that always returns the same timestamp
        # but different values (the new values should be ignored, as the cached result is returned instead)
        proc = TestProcessor((START_VAL, i) for i in range(3))
        for ts, res in proc:
            self.assertTrue((ts == START_VAL and res == START_VAL)) # Expect to always have the same timestamp and result