import json


class EnvNav():

    def __init__(self,
                 conf=None,
                 log=None):
        self.contexts = []
        self.conf = conf
        if conf is None:
            self.conf = dict(name="EnvNav")
        self.log = log
        self.output("Starting", "info")

    def add_context(self, context):
        self.contexts.append(context)

    def get_contexts(self):
        return self.contexts

    def change_value(self, path, value):
        names = path.split("/")
        chg = False
        for k in self.contexts:
            if names[0] == k.__module__:
                nov = k
                for n in names[1:]:
                    nov = getattr(nov, n)
                nov.value = value
            else:
                self.output("path incorrecto " + path, "critical")

    def get_value(self, path):
        names = path.split("/")
        for k in self.contexts:
            if names[0] == k.__module__:
                nov = k
                for n in names[1:]:
                    nov = getattr(nov, n)
                # print nov.value
                return nov.__dict__

    def get_specs(self):
        self.toret = []
        for c in self.contexts:
            self._getPaths(c, c.__module__+"/")
        str = "{\n"
        for s in self.toret:
            str += '\t"' + \
                s.split("/")[len(s.split("/")) - 1] + '":"' + s + '",\n'
        str = str[:len(str) - 2] + "\n}"
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

    def output(self,
               msg,
               lvl="info"):
        if self.log is not None:
            getattr(self.log, lvl)(self.conf["name"] + ": " + str(msg))
