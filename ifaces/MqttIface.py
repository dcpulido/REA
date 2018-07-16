#!/usr/bin/env python
import paho.mqtt
import paho.mqtt.client as mqtt
from paho.mqtt import publish
import threading
import time
import sys
import copy
import json

__author__ = "dcpulido91@gmail.com"


class MqttHand(threading.Thread):
    def __init__(self,
                 conf=None,
                 controller=None,
                 log=None):
        threading.Thread.__init__(self)
        self.log = log
        if conf is not None:
            self.conf = conf
        else:
            self.conf = dict(name=self.__module__,
                             host="localhost",
                             port=1883,
                             timeout=60,
                             subscribe="MqttHand/#")
        self.connected = False
        self.client = mqtt.Client()
        self.controller = controller
        self.buffer = []
        self.output("Start")

    def set_controller(self,
                       cont):
        self.controller = cont

    def run(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.conf["host"],
                            int(self.conf["port"]),
                            int(self.conf["timeout"]))
        self.output("Subscribe "+self.conf["subscribe"])
        self.client.subscribe(self.conf["subscribe"])
        self.client.loop_forever()

    def on_connect(self,
                   client,
                   userdata,
                   flags,
                   rc):
        self.connected = True
        self.output("Connected with result code "+str(rc))

    def on_message(self,
                   client,
                   userdata,
                   msg):
        try:
            payload = json.loads(msg.payload)
        except ValueError:
            payload = msg.payload
        message = dict(topic=msg.topic,
                       payload=msg.payload)
        if self.controller is not None:
            self.controller.parse_message(message)
        else:
            self.buffer.append(message)

    def on_publish(self,
                   path,
                   payload,
                   host="localhost"):
        if host is not None:
            hh = host
        else:
            hh = self.conf["host"]
        publish.single(path,
                       payload,
                       hostname=hh)

    def get_buffer(self):
        toret = copy.deepcopy(self.buffer)
        self.buffer = []
        return toret

    def shutdown(self):
        self.output("Shutdown", "warn")
        self.client.disconnect()
        self.connected = False

    def output(self,
               msg,
               lvl="info"):
        if self.log is not None:
            getattr(self.log, lvl)(self.conf["name"] + ": " + str(msg))
