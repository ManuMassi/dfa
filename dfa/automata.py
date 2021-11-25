from abc import ABC, abstractmethod

EPS = 'eps'


class Automata(ABC):
    def __init__(self, n_states=0, start=None, finals=None, custom_states=None):
        self._n_states = n_states

        self._alphabet = set()

        self._automata = {}
        if not custom_states:
            for state in range(n_states):
                self._automata[state] = {}
        else:
            if not isinstance(custom_states, list) and not isinstance(custom_states, set):
                raise TypeError("You must pass a list or a set of states")
            if not len(custom_states) == self.n_states:
                raise ValueError("The number of custom states it's not equals to n_states")
            for state in custom_states:
                self._automata[state] = {}

        self._states = set(self._automata.keys())
        if start is None:
            start = list(self._automata.keys())[0]
        self.start = start
        self.finals = finals

    def __str__(self):
        automata = ''
        for s in self._automata.__str__().split('},'):
            automata += (s + '}\n')
        return automata

    def __eq__(self, other):
        if not isinstance(other, Automata):
            return False
        same_dict = list(self._automata.items()).sort() == list(other._automata.items()).sort()

        if self.start != other.start:
            print('start')
        if self.finals != other.finals:
            print('finals')
        if self.alphabet != other.alphabet:
            print('alphabet')
        if not same_dict:
            print('not same dict')

        return self.start == other.start and \
            self.finals == other.finals and \
            self.alphabet == other.alphabet and \
            same_dict

    @property
    def n_states(self):
        return self._n_states

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start not in self.states:
            raise ValueError("The state that you selected is not in the automata")
        self._start = start

    @property
    def finals(self):
        return self._finals

    @finals.setter
    def finals(self, finals):
        if finals is None:
            self._finals = set()
        elif isinstance(finals, list) or isinstance(finals, set):
            self._finals = set(finals)
        elif finals in self.states:
            self._finals = {finals}
        else:
            raise TypeError("You must pass the final states as a list or as a single state")

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def states(self):
        return set(self._automata.keys())

    def get_events_from_state(self, state):
        if state not in self.states:
            raise ValueError("The selected state is not in the automata")

        return set(self._automata[state])

    def delta(self, state, event):
        if state not in self.states:
            raise ValueError("The selected state is not in the automata")
        if event not in self.alphabet.union({EPS}):
            raise ValueError("The selected event is not in the alphabet")

        try:
            return self._automata[state][event]
        except KeyError:
            return set()


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
        if state not in self._automata.keys():
            raise IndexError("The state is out of range")
        if transition and (event or nextState) \
                or (not transition and (not event or not nextState)):
            raise AttributeError("Signature error")

        if event and nextState:
            if nextState not in self._automata.keys():
                raise IndexError("The next state is out of range")
            else:
                if event != EPS:
                    self._alphabet.add(event)
        elif isinstance(transition, tuple):
            if transition[1] not in self._automata.keys():
                raise IndexError("The next state is out of range")
            else:
                if transition[0] != 'eps':
                    self._alphabet.add(transition[0])
        elif isinstance(transition, dict):
            for k, v in transition.items():
                if v not in self._automata.keys():
                    raise IndexError(f"The next state {v} is out of range")
                else:
                    if k != EPS:
                        self._alphabet.add(k)

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
