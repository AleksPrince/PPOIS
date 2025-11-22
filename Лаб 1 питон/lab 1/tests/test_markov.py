# tests/test_markov.py
import unittest
from markov.markov import MarkovAlgorithm

class TestMarkovAlgorithm(unittest.TestCase):
    def setUp(self):
        self.rules = [('ab', 'ba'), ('aa', 'a')]
        self.alg = MarkovAlgorithm(self.rules)

    def test_apply_rule(self):
        self.assertEqual(self.alg.apply('ab'), 'ba')

    def test_no_rule(self):
        self.assertEqual(self.alg.apply('xyz'), 'xyz')

    def test_run(self):
        self.assertEqual(self.alg.run('aab'), 'ba')

    def test_stable(self):
        self.assertEqual(self.alg.run('xyz'), 'xyz')

if __name__ == '__main__':
    import unittest
    unittest.main()

