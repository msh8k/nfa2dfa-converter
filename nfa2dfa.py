# Name: Matthew S. Harrison

# implements Figure 3.33 in the Dragon book
def eclosure(T):
    closure = [t for t in T]
    stack = [s for s in T]
    while stack:
        t = states[stack.pop()]  # states is dictionary of NFA from outer scope
        for u in t['E']:
            if u and u not in closure:  # ensure u is not empty string first, then check if in closure
                closure.append(u)
                stack.append(u)
    return set(closure)


def move(T, a):
    moves = []
    for t in T:
        edges = states[t][a]
        if edges:
            for e in edges:
                if e and e not in moves:
                    moves.append(e)
    return set(moves)


# input assumption: file input always the same -- no error handling
initial_states = list(input().split(':')[1].strip())
final_states = list(input().split(':')[1].strip(' {}').split(','))
total_states = int(input().split(':')[1].strip())

inputs = input().split()[1:]
for i in inputs:
    i.strip()

states = {}
for state in range(total_states):
    line = input().split()
    states[line[0]] = dict(zip(inputs, line[1:]))
    for i in inputs:
        states[line[0]][i] = states[line[0]][i].strip(' {}').split(',')

print("reading NFA ... done.\n")
print("creating corresponding DFA ... ")

# Figure 3.32 in the Dragon book - subset construction algorithm - starts here
state_counter = 1                   # for marking new states
current_state = 1                   # for keying transitions in DFA

start = eclosure(initial_states)
d_states = {state_counter: start}
d_inverse_states = {tuple(start): state_counter}
d_final_states = []                 # for displaying final states
print("new DFA state:  " + str(state_counter) + "\t-->  " + str(start))

unmarked = [eclosure(initial_states)]
d_tran = {}
while unmarked:
    current = unmarked.pop()
    current_state = d_inverse_states[tuple(current)]
    for i in inputs:
        if i == 'E':
            continue
        U = eclosure(move(current, i))
        if U and U not in d_states.values():
            state_counter += 1
            d_states[state_counter] = U
            d_inverse_states[tuple(U)] = state_counter
            print("new DFA state:  " + str(state_counter) + "\t-->  " + str(U))
            unmarked.append(U)
            if [f for f in final_states if f in U]:  # check if any of the original final states in new state
                d_final_states.append(state_counter)
        d_tran[(current_state, i)] = U  # need immutable key, so convert to tuple
print("done.\n")

# Display final DFA
print("Final DFA:")
print("Initial State:\t1")  # always 1
print("Final States:\t" + str(d_final_states))
print("Total States:\t" + str(state_counter))
inputs.remove('E')  # remove empty for display purposes
print("State\t" + "".join('{}\t\t\t\t'.format(*x) for x in inputs))
for i in range(1, state_counter+1):
    print(str(i) + "\t\t", end='')
    for j in inputs:
        try:
            print(str("{" + str(d_inverse_states[tuple(d_tran[i, j])]) + "}") + "\t\t\t\t", end='')
        except KeyError:
            print("{}" + "\t\t\t\t", end='')
    print()
