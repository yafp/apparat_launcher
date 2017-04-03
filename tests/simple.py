#!/usr/bin/python
"""apparat - an application launcher for linux"""


# -----------------------------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------------------------

# general
import unittest




# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------------------------
#
# via: http://www.onlamp.com/pub/a/python/2004/12/02/tdd_pyunit.html

# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    # Test: 
    def testOne(self):
        self.failUnless(IsOdd(1))

    # Test: fail if input is odd
    def testTwo(self):
        self.failIf(IsOdd(2))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
