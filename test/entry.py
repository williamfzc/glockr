import unittest
import os


case_dir = os.path.join(os.path.dirname(__file__), 'cases')
discover = unittest.defaultTestLoader.discover(case_dir, pattern='test_*.py')
runner = unittest.TextTestRunner()
runner.run(discover)
