import unittest
import time
import sys
sys.path.insert(0, "../ifaces")
from MqttIface import MqttHand

class TestMqttHand(unittest.TestCase):
    def test_init_connected(self):
        mq = MqttHand()
        self.assertEqual(mq.connected, False)

    def test_init_NoConf_host(self):
        mq = MqttHand()
        self.assertEqual(mq.conf["host"], "localhost")

    def test_init_NoConf_port(self):
        mq = MqttHand()
        self.assertEqual(mq.conf["port"], 1883)

    def test_init_Conf_host(self):
        mq = MqttHand(dict(host="192.169.0.1", port=1884))
        self.assertEqual(mq.conf["host"], "192.169.0.1")

    def test_init_Conf_port(self):
        mq = MqttHand(dict(host="192.169.0.1", port=1884))
        self.assertEqual(mq.conf["port"], 1884)

    def test_start(self):
        mq = MqttHand(dict(host="localhost",
                           port=1883,
                           timeout=60,
                           subscribe="MqttHand"))
        mq.start()
        time.sleep(0.1)
        con = mq.connected
        mq.shutdown()
        self.assertEqual(con, True)

    def test_shutdown(self):
        mq = MqttHand(dict(host="localhost",
                           port=1883,
                           timeout=60,
                           subscribe="MqttHand"))
        mq.start()
        time.sleep(0.1)
        mq.shutdown()
        con = mq.connected
        self.assertEqual(con, False)

    def test_publish(self):
        mq = MqttHand(dict(host="localhost",
                           port=1883,
                           timeout=60,
                           subscribe="MqttHand/#"))
        mq.start()
        time.sleep(0.1)
        mq.on_publish("MqttHand/test",
                      "Hello")
        aux = []
        while aux == []:
            aux = mq.get_buffer()
            time.sleep(0.1)
        mq.shutdown()
        self.assertEqual(aux[0]["payload"],
                         "Hello")

    def test_message_async(self):
        mq = MqttHand(dict(host="localhost",
                           port=1883,
                           timeout=60,
                           subscribe="MqttHand/#"))
        mq.start()
        time.sleep(0.1)
        mq.on_publish("MqttHand/test",
                      "Hello")
        aux = []
        while aux == []:
            aux = mq.get_buffer()
            time.sleep(0.1)
        mq.shutdown()
        self.assertEqual(aux[0]["payload"],
                         "Hello")

    def test_message_sync(self):
        class Controller:
            def __init__(self):
                self.message = None

            def parse_message(self, message):
                self.message = message
        cnt = Controller()
        mq = MqttHand(conf=dict(host="localhost",
                                port=1883,
                                timeout=60,
                                subscribe="MqttHand/#"),
                      controller=cnt)
        mq.start()
        time.sleep(0.2)
        mq.on_publish("MqttHand/test",
                      "Hello")
        mq.shutdown()
        while cnt.message == None:
            pass
        print cnt.message
        self.assertEqual(cnt.message["payload"], "Hello")
unittest.main()