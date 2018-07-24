#!/usr/bin/env python
import sys
import time
import json
import threading
from Generator import Generator
from KBManager import KbExpert

__author__ = "dcpulido91@gmail.com"

# HERE implementar comportaiento de container


class REAContainer(threading.Thread):
    def __init__(self,
                 project=None,
                 iface=None,
                 log=None,
                 conf=None):
        threading.Thread.__init__(self)
        #HERE GESTIONAR archivos de configuracion
        self.generator = Generator(log=log)
        # HERE Analizar mejor manera de instanciar kbExpert
        self.KbEngine = KbExpert(log=log)

        self.iface = iface

        self.project = project
        self.conf = conf
        if conf is None:
            self.conf = dict()
        self.meta = dict()
        self.running = False
        # HERE EnvNav KB all necessary classes

    def run(self):
        print "run"
        self.running = True
        while self.running:
            time.sleep(1)

        print "shutdown"
        self.output("shutdown", "critical")

    def get_meta(self, meta):
        return self.meta

    def build(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def snap_shot(self):
        pass

    def shutdown(self):
        self.running = False

    def output(self,
               msg,
               lvl="info"):
        if self.log is not None:
            getattr(self.log, lvl)(self.conf["name"] + ": " + str(msg))
