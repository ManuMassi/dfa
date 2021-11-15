from dfa.State import State

# dfa = {
#     0: {'a': 1},
#     1: {'a': 2},
#     2: {'a': 2, 'b': 3},
#     3: {'a': 3, 'b': 0}
# }

class DFA:
    def __init__(self, n_states=0, start=0, finals=None, transitions=None):
        self._n_states = n_states
        self._start = start
        self._finals = finals if finals else []

        self._dfa = {}
        for state in range(n_states):
            self._dfa[state] = {}
            # self._dfa[state] = (State(label=state, initial=(state == self._start), final=(state in self._finals)),
            #                    {})
        self._transitions = transitions

    def __str__(self):
        dfa = ''
        for s in self._dfa.__str__().split('},'):
            dfa += (s + '}\n')
        return dfa

    # @property
    # def dfa(self):
    #     return self._dfa

    # @property
    # def dfa(self, dfa):
    #     if not isinstance(dfa, DFA):
    #         raise TypeError("The object is not a DFA")
    #     self._dfa = dfa


    @property
    def n_states(self):
        return self._n_states

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start not in range(self.n_states):
            raise ValueError("The state that you selected is not in the dfa")
        self._start = start

    @property
    def finals(self):
        return self._finals

    @finals.setter
    def finals(self, finals):
        self._finals = finals if finals and isinstance(finals, list) else []

    def set_transition(self, state, transition=None, event=None, nextState=None):
        if state not in range(self.n_states):
            raise IndexError("The state is out of range")
        if transition and (event or nextState) \
                or (not transition and (not event or not nextState)):
            raise AttributeError("Signature error")

        if event and nextState:
            if nextState not in range(self.n_states):
                raise IndexError("The next state is out of range")
            self._dfa[state][event] = nextState
        elif isinstance(transition, tuple):
            if transition[1] not in range(self.n_states):
                raise IndexError("The next state is out of range")
            self._dfa[state][transition[0]] = transition[1]
        elif isinstance(transition, dict):
            for k, v in transition.items():
                if v not in range(self.n_states):
                    raise IndexError(f"The next state {v} is out of range")
                self._dfa[state][k] = v
