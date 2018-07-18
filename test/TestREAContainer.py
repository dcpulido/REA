import sys
import os
import json
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "./test_resources/test/model/")
sys.path.insert(0, "../resources")
from REAContainer import REAContainer
import unittest

class TestREAContainer(unittest.TestCase):
    def test_REAContainer(self):
        container = REAContainer()
        self.assertEqual(container.running, False)

if __name__ == '__main__':
    unittest.main()