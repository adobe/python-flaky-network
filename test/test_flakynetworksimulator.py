import unittest
import flakynetworksimulator

from flakynetworksimulator import flakynetwork

from flakynetworksimulator.flakynetwork  import FlakyNetwork





class test_flakynetwork(unittest.TestCase):
    def test_ping(self):
        fn = FlakyNetwork()
        fn.pingg()




if __name__ == '__main__':
    unittest.main()