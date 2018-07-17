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
                             project_name="default",
                             template_dir="./templates")
        self.log = log

    def build_project(self, name=None):
        toret = {}
        if name is None:
            name = self.conf["project_name"]
        manifest = self.get_manifest(name)
        if manifest != {}:

            toret["rules"] = self.read_rules(name,
                                             manifest)
            toret["varss"] = self.get_vars(toret["rules"])
            toret["context"] = self.generate_context(toret["varss"],
                                                     name,
                                                     manifest)
            toret["context_spec"] = self.generate_context_spec(name,
                                                               manifest)
            return True
        else:
            self.output("Project manifest doesnt exist", "critical")
            return False

    def get_manifest(self,
                     name):
        toret = {}
        try:
            with open(self.conf["project_dir"] +
                      name +
                      "/manifest.json") as data_file:
                toret = json.loads(data_file.read())
            return toret
        except IOError as e:
            return toret

    def read_rules(self,
                   name,
                   manifest):
        rules = []
        if name != manifest["name"]:
            self.output("worng name on manifest or input: " + name,
                        "critical")
            return None
        lst_Dir = os.walk(self.conf["project_dir"] +
                          name +
                          "/" +
                          manifest["conf"]["rules"])
        for l in lst_Dir:
            for rul in l[2]:
                try:
                    with open(self.conf["project_dir"] +
                              name +
                              "/" +
                              manifest["conf"]["rules"] +
                              rul) as data_file:
                        rules.append(json.loads(data_file.read()))
                except ValueError:
                    self.output("json error on " + rul, "critical")
                except IOError:
                    self.output("wrong directorie ", "critical")
        return rules

    def get_vars(self,
                 rules):
        varss = dict(signal=[], status=[])
        if rules is None:
            return varss

        for rul in rules:
            for tr in rul["true"]:
                if tr not in varss["status"]:
                    varss["status"].append(tr)
            for tr in rul["false"]:
                if tr not in varss["status"]:
                    varss["status"].append(tr)
            for tr in rul["value"]:
                if tr not in varss["signal"] and \
                        tr.keys()[0] != "Trigger":
                    if tr[tr.keys()[0]][0] == "$":
                        tr[tr.keys()[0]] = ""
                    varss["signal"].append(tr)
        return varss

    def generate_context(self,
                         varss,
                         name,
                         manifest):
        context_temp = self._get_str_template("context")
        toret = dict(signal="", status="")
        if len(varss["signal"]) == 0:
            toret["signal"] += ESPACES + "pass"
        if len(varss["status"]) == 0:
            toret["status"] += ESPACES + "pass"
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
        with open(self.conf["project_dir"] +
                  name +
                  "/" +
                  manifest["conf"]["model"], 'w+') as ffile:
            ffile.write(tt)
        return tt

    def generate_context_spec(self, name, manifest):

        self.toret = []
        sys.path.insert(0, self.conf["project_dir"] +
                        name +
                        "/" +
                        manifest["conf"]["model"].split("/")[0])
        cc = manifest["conf"]["model"].split("/")[1].split(".")[0]
        exec "from " + cc + " import " + cc
        c = Context()
        self._getPaths(c, c.__module__+"/")
        str = "{\n"
        for s in self.toret:
            str += '\t"' + \
                s.split("/")[len(s.split("/")) - 1] + '":"' + s + '",\n'
        str = str[:len(str) - 2] + "\n}"
        with open(self.conf["project_dir"] + name + "/spec/Context.json", 'w+') as ffile:
            ffile.write(json.dumps(json.loads(str), indent=2))
        return json.loads(str)

    def _getPaths(self, nav, path):
        for k in dir(nav):
            if k[0] != "_":
                if hasattr(getattr(nav, k),
                           'value'):
                    self.toret.append(path + k)
                else:
                    self._getPaths(getattr(nav, k),
                                   path + k + "/")

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
