from dfa import DFA


dfa = DFA(n_states=10, start=0, finals=[8])

#print(dfa)


dfa.set_transition(0, transition=(1,1), event='a')

print(dfa)