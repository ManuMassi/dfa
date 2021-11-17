from dfa import Automata, DFA


# nfa = {
#     0: {'a': [1]},
#     1: {'a': [2]},
#     2: {'a': [2, 3]},
#     3: {'a': [3], 'b': [0, 1]}
# }


class NFA(Automata):
    EPS = 'eps'

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

    # does not work with loops :(
    # def compute_D_eps(self, state):
    #     D_eps = {state}
    #
    #     for event in self._automata[state]:
    #         if event == self.EPS:
    #             for nextState in self._automata[state][event]:
    #                 D_eps.add(nextState)
    #                 D_eps = D_eps.union(self.compute_D_eps(nextState))
    #     return D_eps

    def compute_D_eps(self, state):
        def rec(actualState, D_eps=None):
            if D_eps is None:
                D_eps = set()

            D_eps.add(actualState)

            for event in self._automata[actualState]:
                if event == self.EPS:
                    for nextState in self._automata[actualState][event]:
                        if nextState not in D_eps:
                            return D_eps.union(rec(nextState, D_eps))
            return D_eps

        return rec(state)

    def compute_D_event(self, state, event):
        D_event = set()

        for e in self._automata[state]:
            if e == event:
                for nextState in self._automata[state][event]:
                    D_event.add(nextState)
                    D_event = D_event.union(self.compute_D_eps(nextState))

        return D_event


def nfa2dfa(nfa):
    x_new = [nfa.compute_D_eps(0)]
    X = x_new.copy()

    transitions = []
    while len(x_new) > 0:
        # Select a state x' from x_new
        x_prime = x_new.pop()

        for event in nfa.alphabet:
            alpha = set()
            for state in x_prime:
                alpha = alpha.union(nfa.compute_D_event(state, event))

            if len(alpha) > 0:
                beta = set()
                for state in alpha:
                    beta = beta.union(nfa.compute_D_eps(state))

                if len(beta) > 0:
                    # Save transition found
                    fromState = x_prime.copy()
                    toState = beta.copy()
                    transitions.append((fromState, event, toState))

                    # Save the new state
                    if beta not in X:
                        x_new.append(beta)
                        X.append(beta)

    # Compute final states
    finals = []
    for state_set in X:
        for state in state_set:
            if state in nfa.finals:
                finals.append(state)

    # Creating the dfa
    dfa = DFA(len(X), start=0, finals=finals)

    # Setting transitions
    for transition in transitions:
        dfa.set_transition(X.index(transition[0]), (transition[1], X.index(transition[2])))

    return dfa
