import unittest
from dfa.dfa import DFA
from unittest.mock import patch


class TestDFA(unittest.TestCase):
    @patch("dfa.dfa.DFA.__abstractmethods__", set())
    def setUp(self):
        self.dfa_dict = {
            0: {},
            1: {},
            2: {}
        }
        self.dfa = DFA(n_states=3)

    def test_add_single_transition(self):
        self.dfa_dict[0]['a'] = 1
        self.dfa.set_transition(0, transition=('a', 1))
        self.assertEqual(self.dfa_dict, self.dfa._automata)

        self.dfa_dict[1]['a'] = 1
        self.dfa.set_transition(1, transition={'a': 1})
        self.assertEqual(self.dfa_dict, self.dfa._automata)

        self.dfa_dict[2]['a'] = 1
        self.dfa.set_transition(state=2, event='a', nextState=1)
        self.assertEqual(self.dfa_dict, self.dfa._automata)

        self.assertEqual(self.dfa._automata[0], {'a': 1})

    def test_add_multiple_transition(self):
        self.dfa_dict[0]['a'] = 1
        self.dfa_dict[0]['b'] = 2
        self.dfa.set_transition(state=0, transition={'a': 1, 'b': 2})
        self.assertEqual(self.dfa_dict, self.dfa._automata)
        self.assertEqual(self.dfa._automata[0], {'a': 1, 'b': 2})
        self.dfa.set_transition(0, event='a', nextState=2)
        self.assertEqual(self.dfa._automata[0], {'a': 2, 'b': 2})

    def test_remove_state(self):
        self.dfa.set_transition(0, ('a', 2))
        self.dfa.set_transition(1, {'a': 2, 'b': 2})
        self.dfa.set_transition(2, ('c', 2))

        self.dfa.remove_state(2)
        del self.dfa_dict[2]
        self.assertEqual(self.dfa._automata, self.dfa_dict)
