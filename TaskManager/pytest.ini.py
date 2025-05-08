import unittest


[pytest]

DJANGO_SETTINGS_MODULE = 'TaskManager.settings'


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()
