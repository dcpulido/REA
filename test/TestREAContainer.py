import sys
import os
import json
import time
import copy
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "./test_resources/test/model/")
sys.path.insert(0, "../resources")
from REAContainer import REAContainer
import unittest

class TestREAContainer(unittest.TestCase):
    def test_REAContainer(self):
        container = REAContainer()
        self.assertEqual(container.running, False)

    def test_run_container(self):
        print "TUN"
        container = REAContainer()
        #HERE HILO NO ARRANCA
        container.start()
        time.sleep(0.1)
        aux = copy.deepcopy(container.running)
        print aux
        print container.running
        container.shutdown()
        self.assertEqual(aux, True)

    def test_stop_container(self):
        container = REAContainer()
        container.start()
        container.shutdown()
        self.assertEqual(container.running, False)


if __name__ == '__main__':
    unittest.main()