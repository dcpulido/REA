#!/usr/bin/env python
import threading

__author__ = "dcpulido91@gmail.com"

#HERE implementar comportaiento de container

class REAContainer(threading.Thread):
    def __init__(self,
                 log=None,
                 conf=None):
        threading.Thread.__init__(self)
        self.conf = conf
        if conf is None:
            self.conf = dict()
        self.meta = dict()
        self.running = False
        # HERE EnvNav KB all necessary classes

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


    def output(self,
               msg,
               lvl="info"):
        if self.log is not None:
            getattr(self.log, lvl)(self.conf["name"] + ": " + str(msg))
