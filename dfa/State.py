class State:
    def __init__(self, label='', initial=False, final=False):
        self.label = label
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        if self.initial:
            s = 'Initial '
        if self.final:
            s += 'Final '
        s += f'State {self.label}'

        return s

    def __repr__(self):
        return self.__str__()
