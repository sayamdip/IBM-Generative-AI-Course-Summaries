import unittest

from mymodule3 import square,double

class TestSquare(unittest.TestCase):

    def test1(self):
        self.assertEqual(square(2),4)
        self.assertEqual(square(3.0),9.0)
        self.assertNotEqual(square(-3),-9)
    
class TestDouble(unittest.TestCase):

    def test1(self):
        self.assertEqual(double(2),4)
        self.assertEqual(double(-3.1),-6.2)
        self.assertEqual(double(0),0)
if __name__ == "__main__":
    unittest.main()