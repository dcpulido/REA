#!/usr/bin/env python
import sys
sys.path.insert(0, "./resources")
sys.path.insert(0, "./ifaces")
import logging
import time
import ConfigParser
from colorlog import ColoredFormatter
from HController import HController
from MqttIface import MqttHand


__author__ = "dcpulido91@gmail.com"

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
CONFIG_FILE = "./conf/config.conf"
NAME = "REA"
LOG_ENUM = ["debug", "info", "warn", "error", "critical"]

logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)

log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


def output(msg, lvl="info"):
    getattr(log, lvl)(NAME + ": " + str(msg))


def get_general_conf(name):
    def ConfigSectionMap(section, Config):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
            except:
                output("exception on %s!" % option, LOG_ENUM[2])
                dict1[option] = None
        return dict1
    output(name, LOG_ENUM[0])
    Config = ConfigParser.ConfigParser()
    Config.read(CONFIG_FILE)
    myprior = {}
    for sec in Config.sections():
        if sec == name:
            myprior = ConfigSectionMap(sec, Config)
    return myprior

def shutdown():
    hcont.shutdown()
    iface.shutdown()
if __name__ == '__main__':

    #log.debug("A quirky message only developers care about")
    #log.info("Curious users might want to know this")
    #log.warn("Something is wrong and any user should be informed")
    #log.error("Serious stuff, this is red for a reason")
    #log.critical("OH NO everything is on fire")

    output("System")
    GENERAL_CONF = get_general_conf("GENERAL")
    HCONTROLLER_CONF = get_general_conf("HCONTROLLER")
    MQTT_CONF = get_general_conf("MQTT_IFACE")

    iface = MqttHand(conf=MQTT_CONF,
                     log=log)

    hcont = HController(iface,
                        log,
                        HCONTROLLER_CONF)
    iface.set_controller(hcont)

    try:
        iface.start()
        
        output(hcont.get_projects())
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown()
    except AttributeError, e:
        output(str(e), LOG_ENUM[4])
        shutdown()
