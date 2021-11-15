import unittest
from dfa import DFA


class DfaTest(unittest.TestCase):
    def setUp(self):
        self.dfa_dict = {
            0: {},
            1: {},
            2: {}
        }
        self.dfa = DFA(n_states=3)

    def test_creation_empty(self):
        self.assertEqual(self.dfa_dict, DFA(n_states=3)._dfa)

    def test_start_state(self):
        self.dfa.start = 1

        self.assertEqual(self.dfa.start, 1)
        self.assertFalse(self.dfa.start == 0)
        with self.assertRaises(ValueError):
            self.dfa.start = 3

    def test_final_states(self):
        self.dfa.finals = [0, 1, 2]

        self.assertEqual(self.dfa.finals, [0, 1, 2])
        self.assertFalse(self.dfa.finals == 0)
        self.assertTrue(0 in self.dfa.finals)

    def test_add_single_transition(self):
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0)
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, transition=('a', 1), event='a', nextState=1)
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, transition=('a', 1), nextState=1)
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, transition=('a', 1), event='a')
