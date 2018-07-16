import sys
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "../resources")
from GenericContext import Context
from EnvNav import EnvNav
from KBManager import KbExpert

import unittest

spec = {
    "itsSignal": "GenericContext/Signal/itsSignal",
    "status": "GenericContext/Status/status",
    "Trigger": "GenericContext/Trigger"
}
facts = [{'sys': 'GenericContext',
          'sens': 'Status',
          'values': ['status', 100]},
         {'sys': 'GenericContext',
          'sens': 'Signal',
             'values': ['itsSignal', True]},
         {'sys': 'GenericContext',
          'sens': 'Trigger',
          'values': ['']}
         ]


class TestKBExpert(unittest.TestCase):
    def test_KB(self):
        kb = KbExpert()
        self.assertEqual(kb.conf["name"], "KBExpert")

    def test_set_rules(self):
        kb = KbExpert()
        kb.set_rules("rulename")
        self.assertEqual(kb.rules, "rulename")

    def test_get_env(self):
        gn = Context()
        kb = KbExpert()
        kb.add_context_tree(gn)
        self.assertEqual(kb.get_facts_from_all_contexts(),facts)

    def test_assert_rules(self):
        gn = Context()
        kb = KbExpert()
        kb.add_context_tree(gn)
        kb.assert_rules()



if __name__ == '__main__':
    print "KBEXPERT"
    unittest.main()
