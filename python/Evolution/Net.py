import copy
import random
import re
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


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


def num_flat_features(x):  # 计算矩阵特征数
    size = x.size()[0:]
    num_features = 1
    for s in size:
        num_features *= s
    return num_features


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(225, 300)
        self.fc2 = nn.Linear(300, 225)

    def forward(self, x):
        # 前向传播

        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = F.softmax(x, dim=1)

        return x


def choose(nets):
    global group_cnt
    chessboard, target = build_data()
    fit_v = []
    sum = 0
    for i in range(group_cnt):
        v = fitness(nets[i], chessboard, target)
        fit_v.append(v)
        sum += v
    print(fit_v)
    for i in range(group_cnt):
        fit_v[i] /= sum

    choose_index = []
    for i in range(group_cnt):
        choose_index.append(np.random.choice(range(group_cnt), p=fit_v))

    res = []
    for i in choose_index:
        res.append(copy.deepcopy(nets[i]))

    return res


def build_data():
    data_index = random.sample(range(100), batch_size)
    target = torch.empty([batch_size], dtype=torch.long)
    chessboard = torch.zeros([batch_size, 225])
    for i in range(batch_size):
        step = steps[data_index[i]]
        nowp = random.randint(2, len(step))
        if nowp % 2 == 1:
            nowp -= 1
        now_turn = 1
        for j in range(nowp):
            chessboard[i][step[j]] = now_turn
            now_turn = -now_turn
        target[i] = nowp
    return chessboard, target


def fitness(net, chessboard, target):
    with torch.no_grad():
        out = net(chessboard)
        loss = criterion(out, target)
    return float(loss)


def get_param(net):
    res = np.empty(par_maxcnt)
    cnt = 0
    with torch.no_grad():
        for name, param in net.named_parameters():
            if 'weight' in name:
                for i in range(param.size()[0]):
                    for j in range(param[i].size()[0]):
                        res[cnt] = param[i][j]
                        cnt += 1
            elif 'bias' in name:
                for i in range(param.size()[0]):
                    res[cnt] = param[i]
                    cnt += 1
    return res


def copy_param(net, params):
    cnt = 0
    with torch.no_grad():
        for name, param in net.named_parameters():
            if 'weight' in name:
                for i in range(param.size()[0]):
                    for j in range(param[i].size()[0]):
                        param[i][j] = params[cnt]
                        cnt += 1
            elif 'bias' in name:
                for i in range(param.size()[0]):
                    param[i] = params[cnt]
                    cnt += 1


def cross(net1, net2):
    param1 = get_param(net1)
    param2 = get_param(net2)
    s = np.random.randint(0, par_maxcnt / 2)
    e = np.random.randint(s, par_maxcnt)
    temp = copy.deepcopy(param1[s:e])
    param1[s:e] = copy.deepcopy(param2[s:e])
    param2[s:e] = copy.deepcopy(temp)
    copy_param(net1, param1)
    copy_param(net2, param2)


def mutation(net):
    global par_maxcnt
    p = np.random.rand(par_maxcnt)
    cnt = 0
    with torch.no_grad():
        for name, param in net.named_parameters():
            if 'weight' in name:
                for i in range(param.size()[0]):
                    for j in range(param[i].size()[0]):
                        if p[cnt] < mutation_p:
                            param[i][j] = np.random.random() * np.power(10, np.random.random())
                        cnt += 1
            elif 'bias' in name:
                for i in range(param.size()[0]):
                    param[i] = np.random.random() * np.power(10, np.random.random())
                    cnt += 1


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


batch_size = 64
group_cnt = 10
cross_p = 0.88
mutation_p = 0.01
epochs = 100

temp_net = Net()
par_maxcnt = sum(p.numel() for p in temp_net.parameters() if p.requires_grad)

net_group = [Net() for i in range(group_cnt)]
criterion = nn.CrossEntropyLoss()
for i in range(epochs):
    s = time.time()
    evolution(net_group)
    e = time.time()
    print("cost", e - s, "s")
