
f = open("pg30896.txt", "r")

fl = f.readlines();

groupSize = len(fl)//16;

for gI in range(0, 16):
    out = open("output" + str(gI), "w")
    for line in fl[:(gI*groupSize+groupSize)]:
        out.write(line)
    out.close()
