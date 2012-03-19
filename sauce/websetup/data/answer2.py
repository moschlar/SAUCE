import fileinput

L, R = [], {}

# list from stdin
for line in fileinput.input():
    L.append(float(line))

# sort by absolute value
L.sort(key = lambda x: abs(x))

# sweep
for index in range(len(L)-1):
    if L[index] + L[index+1] == 0:
        R[abs(L[index])] = True

# output
for item in sorted(R):
    print item