from pyke import knowledge_engine
import logging
from EnvNav import EnvNav


class KbExpert:

    def __init__(self,
                 log=None,
                 conf=None):
        self.conf = conf
        if conf is None:
            self.conf = dict(name="KBExpert",
                             rule_name="rules")
        self.log = log
        self.output("Starting", "info")
        self.contexts_tree = EnvNav()
        self.engine = knowledge_engine.engine((__file__, '.rules'))
        self.context_all_facts = []
        self.rules = self.conf["rule_name"]

    def set_rules(self, rules):
        self.rules = rules

    def get_contexts_tree(self):
        return self.contexts_tree

    def set_context_tree(self, tree):
        self.contexts_tree = tree

    def add_context_tree(self, cont):
        self.contexts_tree.add_context(cont)
        self.get_facts_from_all_contexts()

    def get_context_all_facts(self):
        return self.context_all_facts

    def get_facts_from_all_contexts(self):
        self.context_all_facts=[]
        for contexts in self.contexts_tree.get_contexts():
            self.get_env_fromNav(contexts, [contexts.__module__])
        return self.context_all_facts

    def get_env_fromNav(self, model, names):
        fl = True
        for val in model.__dict__.keys():
            if val == "value":
                tup = {"sys": "", "sens": "", "values": ""}
                values = []
                aux = 0
                for n in names:
                    aux = aux + 1
                    if aux == 1:
                        tup["sys"] = n
                    elif aux == 2:
                        tup["sens"] = n
                    else:
                        values.append(n)
                values.append(model.value)
                tup["values"] = values
                self.context_all_facts.append(tup)
                fl = False
        if fl:
            for val in model.__dict__.keys():
                names.append(val)
                model2 = getattr(model, val)
                self.get_env_fromNav(model2, names)
                names.pop()

    def assert_rules(self):
        self.engine.activate(self.rules)
        for e in self.context_all_facts:
            self.engine.assert_(str(e['sys']), str(e['sens']), e['values'])
        try:
            vals, plans = self.engine.prove_1_goal(
                self.rules+'.toret($sens,$value,$ret)')
            toret = dict(vals=vals, plans=plans)
            self.output(vals, "debug")
            self.engine.reset()
            return toret
        except knowledge_engine.CanNotProve:
            toret = dict(vals=None, plans=None)
            self.output("No rules applies", "debug")
            self.engine.reset()
            return toret
        except AssertionError:
            toret = dict(vals=None, plans=None)
            self.output("Assertion Error", "critical")
            self.engine.reset()
            return toret
        self.engine.reset()
        toret = dict(vals=None, plans=None)
        return toret

    def output(self,
               msg,
               lvl="info"):
        if self.log is not None:
            getattr(self.log, lvl)(self.conf["name"] + ": " + str(msg))


if __name__ == "__main__":
    env = EnvNav()
    kb = KbExpert()
