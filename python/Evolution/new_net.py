import re

import numpy as np


def sgf_to_list(path):
    res = []
    pattern1 = re.compile(';B\[(.*?)\];W\[(.*?)\]', re.S)
    with open(path, 'r') as f:
        B_items = re.findall(pattern1, f.read())
        for i in B_items:
            for j in i:
                res.append(
                    (ord(j[0]) - ord('a')) * 15 + ord(j[1]) - ord('a')
                )
    return res


steps = []
for i in range(1, 101):
    steps.append(sgf_to_list('data/' + str(i) + '.sgf'))


class Net():
    def __init__(self):
        self.l1 = self.liner(225, 300)
        self.l2 = self.liner(300, 225)

    def liner(self, in_size, out_size):
        weight = np.random.randn(in_size, out_size)
        bias = np.zeros([in_size, 1])
        layer = {"w": weight, "b": bias}
        return layer

    def forward(self, x):
        x = self.l1["w"].T * x + self.l1["b"]
        x = self.relu(x)
        x = self.l2["w"].T * x + self.l2["b"]
        x = self.softmax(x)
        return x

    def relu(self, x):
        for data in x:
            data[0] = max(data[0], 0)
        return x

    def softmax(self, x):
        x -= np.max(x, axis=1, keepdims=True)
        x = np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)
        return x


def loss(self, input, target):
    res = 0
    for i in range(batch_size):
        res += -np.log(input[np.nonzero(target[i])[0]])
    return res


def fitness():
    chessboard = np.zeros((15, 15), dtype=int)


def choose(nets):
    pass


def cross(net1, net2):
    pass


def mutation(net):
    global par_maxcnt
    p = np.random.rand(par_maxcnt)
    cnt = 0
    for data in net.l1:



def evolution(nets):
    nets = choose(nets)
    is_chosen = False
    c_index = -1
    for i in range(group_cnt):
        p = np.random.random()
        if p < cross_p:
            if is_chosen:
                cross(nets[i], nets[c_index])
                is_chosen = False
            else:
                is_chosen = True
                c_index = i
        mutation(nets[i])


group_cnt = 10
cross_p = 0.88
mutation_p = 0.01
epochs = 100
batch_size = 128

par_maxcnt = 225 * 300 + 300 + 300 * 255 + 255
net_group = [Net() for i in range(group_cnt)]
evolution(net_group)
