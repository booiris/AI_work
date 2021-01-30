import matplotlib.pyplot as plt

cnt = 0
y1 = []
y2 = []
with open("print-e", "r", encoding='utf-8') as f:
    for line in f:
        cnt += 1
        nowp = 0
        while line[nowp] != ' ':
            nowp += 1
        s = nowp
        nowp += 1
        y1.append(float(line[0:s]))
        y2.append(float(line[s:len(line)]))

x = range(cnt)
plt.plot(x, y1, color='b', marker='.', linestyle='-', label='average-fitness')
plt.plot(x, y2, color='r', marker='.', linestyle='-', label='best-fitness')
plt.legend()
plt.savefig('e.png')
plt.show()
