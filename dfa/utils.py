from dfa import NFA, DFA


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

    # Computing final states
    finals = []
    for state_set in X:
        for state in state_set:
            if state in nfa.finals:
                finals.append(X.index(state_set))

    # Creating the dfa
    dfa = DFA(len(X), start=0, finals=finals)

    # Setting transitions
    for transition in transitions:
        dfa.set_transition(X.index(transition[0]), (transition[1], X.index(transition[2])))

    return dfa


def concurrent_composition(g: DFA, h: DFA):
    x_new = {(g.start, h.start)}
    X = [(g.start, h.start)]

    E = g.alphabet.union(h.alphabet)
    g_events = g.alphabet.difference(h.alphabet)
    h_events = h.alphabet.difference(g.alphabet)
    # synchronized_events = g.alphabet.intersection(h.alphabet)

    transitions = []
    while len(x_new) > 0:
        x_prime = x_new.pop()

        for e in E:
            x_found = tuple()
            # print(x_prime)
            if e in g_events:
                if g.delta(x_prime[0], e) != set():
                    x_found = (g.delta(x_prime[0], e), x_prime[1])
            elif e in h_events:
                if h.delta(x_prime[1], e) != set():
                    x_found = (x_prime[0], h.delta(x_prime[1], e))
            else:
                if g.delta(x_prime[0], e) != set() and h.delta(x_prime[1], e) != set():
                    x_found = (g.delta(x_prime[0], e), h.delta(x_prime[1], e))

            if x_found:
                fromState = x_prime
                toState = x_found
                transitions.append((fromState, e, toState))

            if x_found and x_found not in X:
                x_new.add(x_found)
                X.append(x_found)

    finals = []
    for state_pair in X:
        if state_pair[0] in g.finals and state_pair[1] in h.finals:
            finals.append(state_pair)

    final_dfa = DFA(len(X), finals=finals, custom_states=X)
    # Setting transitions
    for transition in transitions:
        final_dfa.set_transition(transition[0], (transition[1], transition[2]))

    return final_dfa
