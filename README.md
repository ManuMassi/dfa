# DFA

A python library that allows to create and manage Deterministic Finite state Automatas and Non-deterministic Finite state Automatas

# Usage

**Basic structure of DFAs and NFAs**  
  
This API represents DFAs and NFAs using **dictionaries**  

After creating a DFA or a NFA using the constructor, a dictionary representing all the states and the transitions will be instantiated.  
This dictionary is an attribute of the class, and it's named *_automata*.  
As you can see it's a private attribute, and that's because you probably won't need to access it directly.  
  
### Example

```python
dfa = {
    0: {'a': 1},
    1: {'a': 2},
    2: {'a': 2, 'b': 3},
    3: {'a': 3, 'b': 0}
 }

nfa = {
    0: {'a': [1]},
    1: {'a': [2]},
    2: {'a': [2, 3]},
    3: {'a': [3], 'b': [0, 1]}
 }
```
The most important attributes that you can access are:
- **_n_states_**: the number of states of the automata -> int
- **_start_**: the initial state -> int
- **_finals_**: the finals states -> list of ints


## Creating a DFA and a NFA
```python
from dfa import DFA, NFA

my_dfa = DFA(n_states=4, start=0, finals=[2,3])

my_nfa = NFA(n_states=4, start=0, finals=[2,3])
```

## Adding transitions
After creating a DFA or a NFA, you have to add transitions between states.

You can do it using the *set_transition()* method on the DFA or NFA object. <br/>
This method can be used in 3 different ways:
1. **You can pass a tuple in the form *(event, nextNode)*:** <br/>
    ```python
       # Adding a transition that goes from state '0' to state '1' with the event 'a'
       my_dfa.set_transition(state=0, transition=('a', 1)) # For NFAs is the same
    ```
   
2. **You can pass a dictionary in the form *{event0: nextNode0, event1: nextNode1, ...}* and so on** 
    ```python
       # Adding two transitions from state '0' that go to states '1' and '2' with 'a' and 'b'
       my_dfa.set_transition(state=0, transition={'a': 1, 'b': 2}) # For NFAs is the same
    ```
3. **You can use the parameters *event* and *nextNode* to add a single transition in an easy way**
    ```python
       # Adding a transition that goes from state '0' to state '1' with the event 'a'
       my_dfa.set_transition(state=0, event='a', nextState=1) # For NFAs is the same
    ```

## Upcoming features

- **Concurrent / Parallel composition**
- **Reachable and Co-reachable states**
- **Conversion from NFA to DFA**
- **Accepted language**
- **Graphical representation**
