import os
import sys
import json
from string import Template
# TODO
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

    def generate_rules(self, meta):
        krb = ""
        for rule in meta["rules"]:
            for key in rule.keys():
                if key != "meta":
                    f = getattr(self, "_krb_"+key)
                    krb += f(meta, meta["templates"][key], rule[key])
        #HERE MONTAR cODIGO

        # print krb

    def _krb_true(self,
                  meta,
                  template,
                  values):
        toret = ""
        for v in values:
            cont, branch, sheet = meta["context_spec"][v].split("/")
            toret += template.safe_substitute(dict(cont=cont,
                                                   branch=branch,
                                                   sheet=sheet))
        return toret

    def _krb_false(self,
                   meta,
                   template,
                   values):
        toret = ""
        for v in values:
            cont, branch, sheet = meta["context_spec"][v].split("/")
            toret += template.safe_substitute(dict(cont=cont,
                                                   branch=branch,
                                                   sheet=sheet))
        return toret

    def _krb_name(self,
                  meta,
                  template,
                  values):
        toret = template.safe_substitute(dict(name=values))
        return toret

    def _krb_toret(self,
                   meta,
                   template,
                   values):
        toret = ""
        toret += template.safe_substitute(dict(name=meta["name"],
                                               result=values["result"],
                                               ret=values["ret"]))
        return toret

    def _krb_call(self,
                  meta,
                  template,
                  values):
        toret = ""
        for v in values:
            toret += template.safe_substitute(dict(stat=v))
        return toret

    def _krb_value(self,
                   meta,
                   template,
                   values):
        toret = ""
        for v in values:
            if meta["context_spec"][v.keys()[0]].split("/")[1] == "Trigger":
                cont, sheet = meta["context_spec"][v.keys()[0]].split("/")
                val = v[v.keys()[0]]
                toret += meta["templates"]["trigger"].safe_substitute(dict(cont=cont,
                                                                           sheet=sheet,
                                                                           val=val))
            else:
                cont, branch, sheet = meta["context_spec"][v.keys()[
                    0]].split("/")
                val = v[v.keys()[0]]
                toret += template.safe_substitute(dict(cont=cont,
                                                       branch=branch,
                                                       sheet=sheet,
                                                       val=val))
        return toret

    def build_meta_project(self, name=None):
        toret = {}
        if name is None:
            name = self.conf["project_name"]
        manifest = self.get_manifest(name)
        if manifest != {}:
            toret["name"] = name
            toret["rules"] = self.read_rules(manifest)
            toret["varss"] = self.get_vars(toret["rules"])
            toret["context"] = self.generate_context(toret["varss"],
                                                     manifest)
            toret["context_spec"] = self.generate_context_spec(manifest)
            toret["manifest"] = manifest
            toret["templates"] = self.generation_templates(toret["manifest"])
            return toret
        else:
            self.output("Project manifest doesnt exist", "critical")
            return False

    def generation_templates(self, manifest):
        toret = {}
        try:
            with open(self.conf["project_dir"] +
                      manifest["name"] + "/" +
                      manifest["conf"]["templates"]) as data_file:
                try:
                    toret = json.loads(data_file.read())
                except ValueError as e:
                    return toret
            for tem in toret.keys():
                toret[tem] = Template(toret[tem])
            return toret
        except IOError as e:
            self.output("Not templates.json on " +
                        manifest["conf"]["templates"], "critical")
            return toret

    def generate_krb_file(self, properties):
        pass

    def get_manifest(self,
                     name):
        toret = {}
        try:
            with open(self.conf["project_dir"] +
                      name +
                      "/manifest.json") as data_file:
                toret = json.loads(data_file.read())
            if name != toret["name"]:
                self.output("worng name on manifest or input: " + name,
                            "critical")
                return {}
            return toret
        except IOError as e:
            return toret

    def read_rules(self,
                   manifest):
        rules = []
        lst_Dir = os.walk(self.conf["project_dir"] +
                          manifest["name"] +
                          "/" +
                          manifest["conf"]["rules"])
        for l in lst_Dir:
            for rul in l[2]:
                try:
                    with open(self.conf["project_dir"] +
                              manifest["name"] +
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
                  manifest["name"] +
                  "/" +
                  manifest["conf"]["model"], 'w+') as ffile:
            ffile.write(tt)
        return tt

    def generate_context_spec(self, manifest):

        self.toret = []
        sys.path.insert(0, self.conf["project_dir"] +
                        manifest["name"] +
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
        with open(self.conf["project_dir"] + manifest["name"] + "/spec/Context.json", 'w+') as ffile:
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
