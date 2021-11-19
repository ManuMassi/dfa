from dfa.automata import Automata


# dfa = {
#     0: {'a': 1},
#     1: {'a': 2},
#     2: {'a': 2, 'b': 3},
#     3: {'a': 3, 'b': 0}
# }


class DFA(Automata):
    def set_transition(self, state, transition=None, event=None, nextState=None):
        super().set_transition(state, transition, event, nextState)

        if event and nextState:
            self._automata[state][event] = nextState
        elif isinstance(transition, tuple):
            self._automata[state][transition[0]] = transition[1]
        elif isinstance(transition, dict):
            for k, v in transition.items():
                self._automata[state][k] = v

        def remove_state(self, state):
            pass

    def remove_state(self, state):
        super().remove_state(state)

        for s in list(self._automata):
            for event in list(self._automata[s]):
                if state == self._automata[s][event]:
                    del self._automata[s][event]


