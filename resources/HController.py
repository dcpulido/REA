import sys
from os import system, walk


class HController:
    def __init__(self,
                 iface,
                 log,
                 conf):
        self.log = log
        self.conf = conf
        self.output("start")
        self.iface = iface
        self.projects = {}
        pp = next(walk(self.conf["project_dir"]))[1]
        for p in pp:
            self.projects[p] = False


    def get_projects(self):
        return self.projects

    def build_project(self):
        pass

    def start_project(self):
        pass

    def stop_project(self):
        pass

    def new_proyect(self,
                    name):
        system("mkdir " + self.conf["project_dir"] + name)
        system("mkdir " + self.conf["project_dir"] + name + "/spec")
        system("mkdir " + self.conf["project_dir"] + name + "/app")
        system("mkdir " + self.conf["project_dir"] + name + "/conf")
        system("mkdir " + self.conf["project_dir"] + name + "/rules")


    def delete_project(self,
                       name):
        system("rm -Rf " + self.conf["project_dir"] + name)

    def output(self,
               msg,
               lvl="info"):
        getattr(self.log, lvl)(self.conf["name"] + ": " + msg)

    def parse_message(self,
                      msg):
        self.output(msg)

    def shutdown(self):
        self.output("Shutdown", "warn")
