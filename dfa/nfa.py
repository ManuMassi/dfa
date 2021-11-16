from dfa import Automata


# dfa = {
#     0: {'a': [1]},
#     1: {'a': [2]},
#     2: {'a': [2, 3]},
#     3: {'a': [3], 'b': [0, 1]}
# }


class NFA(Automata):
    def __init__(self, n_states=0, start=0, finals=None):
        super().__init__(n_states, start, finals)

    def set_transition(self, state, transition=None, event=None, nextState=None):
        super().set_transition(state, transition, event, nextState)

        if event and nextState:
            if event not in self._automata[state]:
                self._automata[state][event] = []
            self._automata[state][event].append(nextState)

        elif isinstance(transition, tuple):

            if transition[0] not in self._automata[state]:
                self._automata[state][transition[0]] = []
            if transition[1] in self._automata[state][transition[0]]:
                raise ValueError("This transition already exists")
            self._automata[state][transition[0]].append(transition[1])

        elif isinstance(transition, dict):
            for e, s in transition.items():
                if event not in self._automata[state]:
                    self._automata[state][e] = []
                self._automata[state][e].append(s)

    def remove_state(self, state):
        super().remove_state(state)

        for s in list(self._automata):
            for event in list(self._automata[s]):
                if state in self._automata[s][event]:
                    del self._automata[s][event]