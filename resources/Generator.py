import os
import sys
import json
from string import Template
# TODO
# read manifest to change rutes inside project
# generate the krb
# define responses
# define torets


ESPACES = "    "


class Generator:
    def __init__(self,
                 conf=None,
                 log=None):
        self.conf = conf
        if conf is None:
            self.conf = dict(project_dir="./projects/",
                             project_name="",
                             template_dir="./templates")
        self.rules = []
        self.templates = {}
        self.context = {}
        self.vars = {}

    def read_spec_templates(self, name=None):
        if name is None:
            name = self.conf["project_name"]
        pass

    def read_spec_context(self, name=None):
        if name is None:
            name = self.conf["project_name"]
        pass

    def read_spec_imperative(self, name=None):
        if name is None:
            name = self.conf["project_name"]
        pass

    def read_rules(self,
                   name=None):
        self.rules = []
        if name is None:
            name = self.conf["project_name"]
        lst_Dir = os.walk(self.conf["project_dir"] +
                          name +
                          "/rules")
        for l in lst_Dir:
            for rul in l[2]:
                try:
                    with open(self.conf["project_dir"] +
                              name +
                              "/rules/" +
                              rul) as data_file:
                        self.rules.append(json.loads(data_file.read()))
                except ValueError:
                    self.output("json error on " + rul, "critical")
        return self.rules

    def get_vars(self, rules=None):
        self.vars = dict(signal=[], status=[])
        if rules is None:
            rules = self.rules

        for rul in rules:
            for tr in rul["true"]:
                if tr not in self.vars["status"]:
                    self.vars["status"].append(tr)
            for tr in rul["false"]:
                if tr not in self.vars["status"]:
                    self.vars["status"].append(tr)
            for tr in rul["value"]:
                if tr not in self.vars["signal"] and \
                        tr.keys()[0] != "Trigger":
                    if tr[tr.keys()[0]][0] == "$":
                        tr[tr.keys()[0]] = ""
                    self.vars["signal"].append(tr)
        return self.vars

    def generate_context(self,
                         varss,
                         name=None):
        if name is None:
            name = self.conf["project_name"]
        context_temp = self._get_str_template("context")
        toret = dict(signal="", status="")
        for sig in varss["signal"]:
            if type(sig[sig.keys()[0]]) is str:
                sig[sig.keys()[0]] = "\"\""

            toret["signal"] += ESPACES + \
                "self." +\
                sig.keys()[0] +\
                "=" + \
                "obj(" +\
                sig[sig.keys()[0]] + \
                ")\n"

        for sig in varss["status"]:
            toret["status"] += ESPACES + \
                "self." +\
                sig +\
                "=obj(False)\n"
        tt = context_temp.safe_substitute(toret)
        with open(self.conf["project_dir"] + name + "/model/Context.py", 'w+') as ffile:
            ffile.write(tt)
        return tt

    def generate_context_spec(self, name=None):
        if name is None:
            name = self.conf["project_name"]

        def _getPaths(nav, path):
            for k in dir(nav):
                if k[0] != "_":
                    if hasattr(getattr(nav, k),
                               'value'):
                        self.toret.append(path + k)
                    else:
                        _getPaths(getattr(nav, k),
                                  path + k + "/")
        self.toret = []
        sys.path.insert(0, self.conf["project_dir"] + name + "/model/")
        from Context import Context
        c = Context()
        _getPaths(c, c.__module__+"/")
        str = "{\n"
        for s in self.toret:
            str += '\t"' + \
                s.split("/")[len(s.split("/")) - 1] + '":"' + s + '",\n'
        str = str[:len(str) - 2] + "\n}"
        with open(self.conf["project_dir"] + name + "/spec/Context.json", 'w+') as ffile:
            ffile.write(json.dumps(json.loads(str), indent=2))
        return json.loads(str)

    def _get_str_template(self, name):
        with open(self.conf["template_dir"] +
                  name +
                  ".template") as f:
            template = Template(f.read())
            f.close()
        return template

    def output(self,
               msg,
               lvl="info"):
        if self.log is not None:
            getattr(self.log, lvl)(self.conf["name"] + ": " + str(msg))
