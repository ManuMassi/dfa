import unittest
from unittest.mock import patch
from dfa.automata import Automata


class TestAutomata(unittest.TestCase):

    @patch("dfa.automata.Automata.__abstractmethods__", set())
    def setUp(self):
        self.automata_dict = {
            0: {},
            1: {},
            2: {}
        }
        self.automata = Automata(n_states=3)

    @patch("dfa.automata.Automata.__abstractmethods__", set())
    def test_creation_empty(self):
        self.assertEqual(self.automata_dict, Automata(n_states=3)._automata)

    def test_start_state(self):
        self.automata.start = 1

        self.assertEqual(self.automata.start, 1)
        self.assertFalse(self.automata.start == 0)
        with self.assertRaises(ValueError):
            self.automata.start = 3

    def test_final_states(self):
        self.automata.finals = [0, 1, 2]

        self.assertEqual(self.automata.finals, [0, 1, 2])
        self.assertFalse(self.automata.finals == 0)
        self.assertTrue(0 in self.automata.finals)

    def test_add_transition_signature(self):
        with self.assertRaises(AttributeError):
            self.automata.set_transition(state=0)
            self.automata.set_transition(state=0, transition=('a', 1), event='a', nextState=1)
            self.automata.set_transition(state=0, transition=('a', 1), nextState=1)
            self.automata.set_transition(state=0, transition=('a', 1), event='a')
            self.automata.set_transition(state=0, event='a')
            self.automata.set_transition(state=0, nextState=1)

    def test_add_transition_index(self):
        with self.assertRaises(IndexError):
            self.automata.set_transition(state=3, transition=('a', 0))
            self.automata.set_transition(state=0, transition=('a', 3))
            self.automata.set_transition(state=3, transition=('a', 3))
            self.automata.set_transition(state=0, transition={'a': 3})
            self.automata.set_transition(state=0, transition={'a': 1, 'b': 4})
            self.automata.set_transition(state=0, event='a', nextState=4)

    def test_add_state(self):
        self.automata.add_state()
        self.assertEqual(self.automata.n_states, 4)
        self.automata_dict[3] = {}
        self.assertEqual(self.automata_dict, self.automata._automata)

    def test_remove_state(self):
        self.automata.remove_state(0)
        self.assertEqual(self.automata.n_states, 2)
        with self.assertRaises(KeyError):
            a = self.automata._automata[0]
