import unittest
import sys
sys.path.insert(0, "./test_resources")
sys.path.insert(0, "../dbcon")

from MysqlDAO import MysqlDAO, Instance
class TestMysqlDAO(unittest.TestCase):
    def test_instance_to_dict(self):
        ini = dict(name="name",
                   tlf=88)
        ins = Instance(ini)
        self.assertEqual(ins.to_dict(), ini)

    def test_instance_constructor(self):
        ini = dict(name="name",
                   tlf=88)
        ins = Instance(ini)
        self.assertEqual(ins.name, "name")

    def test_instance_set_by_dict(self):
        ini = dict(name="name",
                   tlf=88)
        ins = Instance()
        ins.set_by_dic(ini)
        self.assertEqual(ins.to_dict(), ini)

unittest.main()