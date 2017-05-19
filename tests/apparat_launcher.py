#!/usr/bin/python
"""apparat_launcher - an application launcher for linux"""

import unittest
import apparat_launcher

class TestFactorial(unittest.TestCase):
    """
    Our basic test class
    """

    def test_fact(self):
        """
        The actual test.
        Any method which starts with ``test_`` will considered as a test case.
        """
        #res = fact(5)
        #self.assertEqual(res, 120)


if __name__ == '__main__':
    unittest.main()
