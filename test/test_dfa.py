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

    def test_add_transition_signature(self):
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0)
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, transition=('a', 1), event='a', nextState=1)
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, transition=('a', 1), nextState=1)
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, transition=('a', 1), event='a')
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, event='a')
        with self.assertRaises(AttributeError):
            self.dfa.set_transition(state=0, nextState=1)

    def test_add_transition_index(self):
        with self.assertRaises(IndexError):
            self.dfa.set_transition(state=3, transition=('a', 0))
        with self.assertRaises(IndexError):
            self.dfa.set_transition(state=0, transition=('a', 3))
        with self.assertRaises(IndexError):
            self.dfa.set_transition(state=3, transition=('a', 3))
        with self.assertRaises(IndexError):
            self.dfa.set_transition(state=0, transition={'a': 3})
        with self.assertRaises(IndexError):
            self.dfa.set_transition(state=0, transition={'a': 1, 'b': 4})
        with self.assertRaises(IndexError):
            self.dfa.set_transition(state=0, event='a', nextState=4)

    def test_add_single_transition(self):
        self.dfa_dict[0]['a'] = 1
        self.dfa.set_transition(0, transition=('a', 1))
        self.assertEqual(self.dfa_dict, self.dfa._dfa)

        self.dfa_dict[1]['a'] = 1
        self.dfa.set_transition(1, transition={'a': 1})
        self.assertEqual(self.dfa_dict, self.dfa._dfa)

        self.dfa_dict[2]['a'] = 1
        self.dfa.set_transition(state=2, event='a', nextState=1)
        self.assertEqual(self.dfa_dict, self.dfa._dfa)

    def test_add_multiple_transition(self):
        self.dfa_dict[0]['a'] = 1
        self.dfa_dict[0]['b'] = 2
        self.dfa.set_transition(state=0, transition={'a': 1, 'b': 2})
        self.assertEqual(self.dfa_dict, self.dfa._dfa)


