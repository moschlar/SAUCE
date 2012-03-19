import fileinput

L, R, D = [], {}, {}

# list from stdin
for line in fileinput.input():
    L.append(float(line))

# symmetric hashing
for item in L:
    if abs(item) in D and D[abs(item)] == -item:
        R[abs(item)] = True
    else:
        D[abs(item)] = item

        # output
for item in sorted(R):
    print item