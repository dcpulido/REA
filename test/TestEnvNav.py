import sys
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "../resources")
from GenericContext import Context
from EnvNav import EnvNav

import unittest

spec = {
    "itsSignal": "GenericContext/Signal/itsSignal",
    "status": "GenericContext/Status/status",
    "Trigger": "GenericContext/Trigger"
}


class TestEnvNav(unittest.TestCase):
    def test_addget_context(self):
        gn = Context()
        env = EnvNav()
        num1 = len(env.get_contexts())
        env.add_context(gn)
        self.assertEqual(num1 + 1,
                         len(env.get_contexts()))

    def test_itsSignal_type(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["itsSignal"])
        self.assertEqual(aux["type"], type(True))

    def test_itsSignal_value(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["itsSignal"])
        self.assertEqual(aux["value"], True)

    def test_Status_type(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["status"])
        self.assertEqual(aux["type"], type(1))

    def test_Status_value(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["status"])
        self.assertEqual(aux["value"], 100)

    def test_Trigger_type(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["Trigger"])
        self.assertEqual(aux["type"], type("asd"))

    def test_Trigger_value(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["Trigger"])
        self.assertEqual(aux["value"], "")

    def test_change_value(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        aux = env.get_value(spec["Trigger"])
        env.change_value(spec["Trigger"], "hola")
        self.assertEqual(env.get_value(spec["Trigger"])["value"], "hola")
    
    def test_get_paths(self):
        gn = Context()
        env = EnvNav()
        env.add_context(gn)
        self.assertEqual(env.get_specs(), spec)


if __name__ == '__main__':
    print "TEST ENVNAV"
    unittest.main()
