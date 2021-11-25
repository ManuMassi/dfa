import unittest
from dfa import DFA, NFA, EPS
from dfa.utils import nfa2dfa, concurrent_composition, draw_automata


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.nfa = NFA(n_states=4, start=0)
        self.nfa.set_transition(0, ('a', 1))
        self.nfa.set_transition(1, {'a': 3, self.nfa.EPS: 2})
        self.nfa.set_transition(2, {'c': 0, self.nfa.EPS: 3})
        self.nfa.set_transition(3, {'b': 2, self.nfa.EPS: 0})

    def test_compute_D_eps(self):
        self.assertEqual(self.nfa.compute_D_eps(0), {0})
        self.assertEqual(self.nfa.compute_D_eps(1), {0, 1, 2, 3})
        self.assertEqual(self.nfa.compute_D_eps(2), {0, 2, 3})
        self.assertEqual(self.nfa.compute_D_eps(3), {0, 3})

        loop_nfa = NFA(2)
        loop_nfa.set_transition(0, (loop_nfa.EPS, 1))
        loop_nfa.set_transition(1, (loop_nfa.EPS, 0))
        self.assertEqual(loop_nfa.compute_D_eps(0), {0, 1})
        self.nfa.set_transition(0, (self.nfa.EPS, 1))

    def test_compute_D_event(self):
        self.assertEqual(self.nfa.compute_D_event(0, 'a'), {0, 1, 2, 3})
        self.assertEqual(self.nfa.compute_D_event(1, 'a'), {0, 3})
        self.assertEqual(self.nfa.compute_D_event(2, 'a'), set())
        self.assertEqual(self.nfa.compute_D_event(3, 'a'), set())

        self.assertEqual(self.nfa.compute_D_event(0, 'b'), set())
        self.assertEqual(self.nfa.compute_D_event(1, 'b'), set())
        self.assertEqual(self.nfa.compute_D_event(2, 'b'), set())
        self.assertEqual(self.nfa.compute_D_event(3, 'b'), {0, 2, 3})

        self.assertEqual(self.nfa.compute_D_event(0, 'c'), set())
        self.assertEqual(self.nfa.compute_D_event(1, 'c'), set())
        self.assertEqual(self.nfa.compute_D_event(2, 'c'), {0})
        self.assertEqual(self.nfa.compute_D_event(3, 'c'), set())

        self.nfa.set_transition(1, ('c', 0))
        self.nfa.set_transition(0, (self.nfa.EPS, 1))
        self.assertEqual(self.nfa.compute_D_event(1, 'c'), {0, 1, 2, 3})

    def test_nfa2dfa(self):
        nfa = NFA(4, finals=[0, 2])
        nfa.set_transition(0, ('b', 1))
        nfa.set_transition(0, ('b', 2))
        nfa.set_transition(1, ('a', 0))
        nfa.set_transition(2, ('a', 2))
        nfa.set_transition(2, (nfa.EPS, 3))
        nfa.set_transition(3, {'b': 3, nfa.EPS: 0})

        dfa = DFA(3, finals=['{0}', '{0, 1, 2, 3}', '{0, 2, 3}'], custom_states=['{0}', '{0, 1, 2, 3}', '{0, 2, 3}'])
        dfa.set_transition('{0}', ('b', '{0, 1, 2, 3}'))
        dfa.set_transition('{0, 1, 2, 3}', {'a': '{0, 2, 3}', 'b': '{0, 1, 2, 3}'})
        dfa.set_transition('{0, 2, 3}', {'a': '{0, 2, 3}', 'b': '{0, 1, 2, 3}'})

        self.assertEqual(nfa2dfa(nfa), dfa)

        nfa = NFA(6, finals=[0])
        nfa.set_transition(0, ('a', 1))
        nfa.set_transition(0, ('a', 3))
        nfa.set_transition(1, (nfa.EPS, 2))
        nfa.set_transition(2, ('c', 5))
        nfa.set_transition(3, (nfa.EPS, 4))
        nfa.set_transition(4, {'b': 4, 'c': 5})
        nfa.set_transition(5, {'a': 5, 'b': 0})

        dfa = DFA(4, finals=['{0}'], custom_states=['{0}', '{1, 2, 3, 4}', '{4}', '{5}'])
        dfa.set_transition('{0}', ('a', '{1, 2, 3, 4}'))
        dfa.set_transition('{1, 2, 3, 4}', {'b': '{4}', 'c': '{5}'})
        dfa.set_transition('{4}', {'b': '{4}', 'c': '{5}'})
        dfa.set_transition('{5}', {'a': '{5}', 'b': '{0}'})

        self.assertEqual(nfa2dfa(nfa), dfa)

    def test_concurrent_composition(self):
        dfa1 = DFA(4, finals=[0])
        dfa1.set_transition(0, ('a', 1))
        dfa1.set_transition(1, ('b', 2))
        dfa1.set_transition(2, ('c', 3))
        dfa1.set_transition(3, {'a': 0, 'b': 3})

        dfa2 = DFA(2, finals=[0, 1])
        dfa2.set_transition(0, ('b', 1))
        dfa2.set_transition(1, {'c': 1, 'd': 0})

        states = [(0, 0), (1, 0), (2, 1), (3, 1), (2, 0), (0, 1), (3, 0), (1, 1)]
        composition = DFA(8, finals=[(0, 0), (0, 1)], custom_states=states)
        composition.set_transition((0, 0), {'a': (1, 0)})
        composition.set_transition((1, 0), {'b': (2, 1)})
        composition.set_transition((2, 1), {'c': (3, 1), 'd': (2, 0)})
        composition.set_transition((3, 1), {'a': (0, 1), 'd': (3, 0)})
        composition.set_transition((0, 1), {'a': (1, 1)})
        composition.set_transition((0, 1), {'d': (0, 0)})
        composition.set_transition((3, 0), {'a': (0, 0), 'b': (3, 1)})
        composition.set_transition((1, 1), {'d': (1, 0)})

        self.assertEqual(composition, concurrent_composition(dfa1, dfa2))

    def test_draw_automata(self):
        dfa = DFA(4, finals=[0])
        dfa.set_transition(0, ('a', 1))
        dfa.set_transition(1, {'b': 2, 'c': 3})
        dfa.set_transition(2, {'b': 2, 'c': 3})
        dfa.set_transition(3, {'a': 3, 'b': 0})

        draw_automata(dfa)

        nfa = NFA(6, finals=[0])
        nfa.set_transition(0, ('a', 1))
        nfa.set_transition(0, ('a', 3))
        nfa.set_transition(1, (EPS, 2))
        nfa.set_transition(2, ('c', 5))
        nfa.set_transition(3, (EPS, 4))
        nfa.set_transition(4, {'b': 4, 'c': 5})
        nfa.set_transition(5, {'a': 5, 'b': 0})

        draw_automata(nfa)


























