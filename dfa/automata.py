from abc import ABC, abstractmethod


class Automata(ABC):
    def __init__(self, n_states=0, start=0, finals=None):
        self._n_states = n_states
        self._start = start
        self._finals = finals if finals else []

        self._automata = {}
        for state in range(n_states):
            self._automata[state] = {}

    def __str__(self):
        automata = ''
        for s in self._automata.__str__().split('},'):
            automata += (s + '}\n')
        return automata

    @property
    def n_states(self):
        return self._n_states

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start not in range(self.n_states):
            raise ValueError("The state that you selected is not in the automata")
        self._start = start

    @property
    def finals(self):
        return self._finals

    @finals.setter
    def finals(self, finals):
        self._finals = finals if finals and isinstance(finals, list) else []


    @abstractmethod
    def set_transition(self, state, transition=None, event=None, nextState=None):
        """
        This method allows you to set a transition using 3 different notation:
        1) By passing a tuple in this form (event, nextState) to the parameter transition you don't need to pass event and nextState
        2) By passing a dictionary {event0: nextState0, event1: nexState1, ...) to the parameter transition you don't need to pass event and nextState
        3) You can ignore the transition parameter and pass event and nextState separately

        :param state: the starting state
        :param transition: a tuple (event, nextState) or a dictionary {event0: nextState0, event1: nexState1, ...)
        :param event: the event for the transition
        :param nextState: the state you want to go
        """
        if state not in range(self.n_states):
            raise IndexError("The state is out of range")
        if transition and (event or nextState) \
                or (not transition and (not event or not nextState)):
            raise AttributeError("Signature error")

        if event and nextState:
            if nextState not in range(self.n_states):
                raise IndexError("The next state is out of range")
        elif isinstance(transition, tuple):
            if transition[1] not in range(self.n_states):
                raise IndexError("The next state is out of range")
        elif isinstance(transition, dict):
            for k, v in transition.items():
                if v not in range(self.n_states):
                    raise IndexError(f"The next state {v} is out of range")

    def add_state(self):
        self._automata[self.n_states] = {}
        self._n_states += 1

    @abstractmethod
    def remove_state(self, state):
        del self._automata[state]

        self._n_states -= 1

        if state in self.finals:
            self._finals.remove(state)
        if self.start == state:
            self.start = list(self._automata.keys())[0]
