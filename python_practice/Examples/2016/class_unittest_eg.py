import unittest
import os
import json
import sys

sys.path.append('../../employee')
from employee import employee

class TestEmployee(unittest.TestCase):
  """
  Unit tests for Employee class

  """
  @unittest.skipIf(3 > 2,
                     "Example 1:Skip test")
  def test_skip_1(self):
    print "skipped"

  @unittest.skipUnless(sys.platform.startswith("win"), "Example 2: Skip test")
  def test_skip_2(self):
    print "skipped"

  # This test wont be counted as failure if it fails.
  @unittest.expectedFailure
  def test_empCount_1(self):
    e = employee.Employee('Har',2, 'HR')
    self.assertEqual(employee.Employee.count, 3)

  @unittest.skip("Example 3: Employee count is not constant, will fix later")
  def test_empCount_2(self):
    e = employee.Employee('Har',2, 'HR')
    self.assertEqual(employee.Employee.count, 3)

  def test_displayEmployee(self):
    e = employee.Employee('Jag',1, 'Tech')
    self.assertEqual(e.name, 'Jag')
    self.assertEqual(e.dept, 'Tech')

  def test_dump_to_file(self):
    e = employee.Employee('XYZ',3, 'Finance')
    file  = '/tmp/emp_info.txt'
    e.dump_to_file(file)
    f = open(file, 'r')
   # print "-----------> File read full file: ", f.read()
   # print "-----------> File read one line: ", f.readline()

 # Read all lines into a list
    for l in f.readlines():
      print "--> line: ", l
      self.assertEqual(l,'XYZ')

    f.close()
    os.remove(file)
    self.assertFalse(os.path.isfile(file))

  def test_dump_json(self):
    e = employee.Employee('ABC',4, 'Finance')
    file  = '/tmp/emp_info.json'
    e.dump_json(file)

    f = open(file, 'r')
    info = json.load(f)
    f.close()

    self.assertEqual(int(info['id']), 4)
    self.assertEqual(str(info['name']), 'ABC')

    os.remove(file)
    self.assertFalse(os.path.isfile(file))

if __name__ == '__main__':
  unittest.main()
