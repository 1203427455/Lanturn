import unittest

def thingy():
    counter = 0
    for i in range(10):
        yield i

def thingy_parent():
    for thing in thingy():
        a = yield thing
        print 'thingy_parent: {}'.format(a)


class BehaviorTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        for thing in thingy_parent():
            print 'test_basic: {}'.format(thing)

if __name__ == '__main__':
    unittest.main()
