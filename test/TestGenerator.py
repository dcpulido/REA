import sys
import os
import json
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "./test_resources/test/model/")
sys.path.insert(0, "../resources")
from GenericContext import Context
from Generator import Generator

import unittest

conf = dict(project_dir="./test_resources/",
            project_name="test",
            template_dir="./test_resources/",
            output_dir="./test_resources/")

rule = {
    "name": "GenericRuleName",
    "true": [
        "itsSignal"
    ],
    "false": [],
    "value": [
        {
            "Trigger": "welcome"
        },
        {
            "status": "$stat"
        }
    ],
    "call": [
        "exp.somethin()",
        "exp.something2()"
    ],
    "toret": {
        "ret": "ex.toret()",
        "result": "ex.result()"
    },
    "meta": {
        "priority": 0
    }
}

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

varss = {'status': ['itsSignal'], 'signal': [{'status': '$stat'}]}

krb_output = """GenericRuleName\n\ttoret(test,ex.result(),ex.toret())\n\twhen\n\t\tContext.Status(itsSignal,True)\n\t\tContext.Trigger(welcome)\n\t\tContext.Signal(status,$stat)\n\t\tpython(exp.somethin())\n\t\tpython(exp.something2())\n\n\nbc_extras\n    import os\n    import json\n    import sys\n    import thread\n    from paho.mqtt import publish\n    sys.path.insert(0, './resources/')\n    sys.path.insert(0, './ifaces/')\n    sys.path.insert(0, './dbcon/')\n    sys.path.insert(0, './modules/')\n    """
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
        aux = False
        try:
            from Context import Context
            aux = True
        except ImportError:
            aux = False
        self.assertEqual(aux, True)

    def test_get_template(self):
        gen = Generator(conf)
        self.assertEqual(gen._get_str_template(
            "context").safe_substitute({}), template)

    def test_buid_project(self):
        gen = Generator(conf)
        self.assertNotEqual(gen.build_meta_project(), False)

    def test_generation_templates(self):
        gen = Generator(conf)
        temp = gen.generation_templates(gen.get_manifest("test"))
        self.assertNotEqual(temp, {})

    def test_generation_rules(self):
        gen = Generator(conf)
        gen.generate_rules(gen.build_meta_project())

    def test_krb_true(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        temp = gen.generation_templates(meta["manifest"])
        self.assertEqual(gen._krb_true(meta, temp["true"], meta["rules"][0]["true"]),
                         "\t\tContext.Status(itsSignal,True)\n")

    def test_krb_false(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        temp = gen.generation_templates(meta["manifest"])
        self.assertEqual(gen._krb_false(meta, temp["false"], meta["rules"][0]["true"]),
                         "\t\tContext.Status(itsSignal,False)\n")

    def test_krb_name(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        temp = gen.generation_templates(meta["manifest"])
        self.assertEqual(gen._krb_name(meta, temp["name"], "test"),
                         "test\n")

    def test_krb_toret(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        temp = gen.generation_templates(meta["manifest"])
        self.assertEqual(gen._krb_toret(meta, temp["toret"], meta["rules"][0]["toret"]),
                         "\ttoret(test,ex.result(),ex.toret())\n")

    def test_krb_call(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        temp = gen.generation_templates(meta["manifest"])
        self.assertEqual(gen._krb_call(meta, temp["call"], meta["rules"][0]["call"]),
                         "\t\tpython(exp.somethin())\n\t\tpython(exp.something2())\n")

    def test_krb_value(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        temp = gen.generation_templates(meta["manifest"])
        self.assertEqual(gen._krb_value(meta, temp["value"], meta["rules"][0]["value"]),
                         "\t\tContext.Trigger(welcome)\n\t\tContext.Signal(status,$stat)\n")

    def test_order_krb(self):
        gen = Generator(conf)
        krb = [dict(meta=dict(priority=2)),
               dict(meta=dict(priority=0)),
               dict(meta=dict(priority=1))]
        self. assertEqual(gen._order_krb(krb), [dict(meta=dict(priority=0)),
                                                dict(meta=dict(priority=1)),
                                                dict(meta=dict(priority=2))])

    def test_generate_str_krb(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        self.assertEqual(gen.generate_rules(meta), krb_output)

    def test_krb_output(self):
        gen = Generator(conf)
        meta = gen.build_meta_project()
        self.assertNotEqual(gen.generate_rules(meta), False)


if __name__ == '__main__':
    print "GENERATOR"
    unittest.main()
