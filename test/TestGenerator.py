import sys
import os
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "./test_resources/test/model/")
sys.path.insert(0, "../resources")
from GenericContext import Context
from Generator import Generator

import unittest

conf = dict(project_dir="./test_resources/",
            project_name="test",
            template_dir="./test_resources/")

rule = {'priority': 0, 'false': [], 'true': ['itsSignal'],
        'name': 'GenericRuleName', 'value': [{'Trigger': 'welcome'}, {'status': '$stat'}]}

template = """class obj:
    def __init__(self, value):
        self.type = type(value)
        self.value = value

    def __dict__(self):
        return dict(type=self.type,
                    value=self.value)


class Signal:
    def __init__(self):
        $signal


class Status:
    def __init__(self):
        $status


class Context:
    def __init__(self):
        self.Signal = Signal()
        self.Status = Status()
        self.Trigger = obj("")"""

spec = {
  "status": "Context/Signal/status", 
  "Trigger": "Context/Trigger", 
  "itsSignal": "Context/Status/itsSignal"
}

varss = {'status': ['itsSignal'], 'signal': [{'status': ''}]}

class TestGenerator(unittest.TestCase):
    def test_Gen(self):
        gen = Generator(conf=conf)
        self.assertEqual(gen.conf["project_dir"], "./test_resources/")

    def test_get_manifest(self):
        gen = Generator(conf)
        self.assertNotEqual(gen.get_manifest("test"), {})

    def test_not_get_manifest(self):
        gen = Generator(conf)
        self.assertEqual(gen.get_manifest("tost"), {})

    def test_read_rules(self):
        gen = Generator(conf=conf)
        man = gen.get_manifest("test")
        self.assertEqual(gen.read_rules(man)[0], rule)

    def test_get_vars(self):
        gen = Generator(conf)
        rul = gen.read_rules(gen.get_manifest("test"))
        self.assertEqual(gen.get_vars(rul), varss)

    def test_not_get_vars(self):
        gen = Generator(conf)
        self.assertEqual(gen.get_vars(None)["signal"], [])

    def test_generate_context(self):
        gen = Generator(conf)
        rul = gen.read_rules(gen.get_manifest("test"))
        gen.generate_context(gen.get_vars(rul), gen.get_manifest("test"))
        aux =False
        try:
            from Context import Context
            aux = True
        except ImportError:
            aux = False
        self.assertEqual(aux,True)

    def test_get_template(self):
        gen = Generator(conf)
        self.assertEqual(gen._get_str_template("context").safe_substitute({}),template)

    def test_buid_project(self):
        gen = Generator(conf)
        self.assertEqual(gen.build_project(), True)

    def test_generation_templates(self):
        gen = Generator(conf)
        temp = gen.generation_templates(gen.get_manifest("test"))
        self.assertNotEqual(temp, {})


if __name__ == '__main__':
    print "GENERATOR"
    unittest.main()
