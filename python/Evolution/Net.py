import copy
import time
from ctypes import *

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def num_flat_features(x):  # 计算矩阵特征数
    size = x.size()[0:]
    num_features = 1
    for s in size:
        num_features *= s
    return num_features


def check(nx, ny, mat, turn):
    temp = [[] for _ in range(4)]
    for i in range(-4, 5):
        if 0 <= nx + i <= 14:
            temp[0].append(mat[nx + i][ny])
    for i in range(-4, 5):
        if 0 <= ny + i <= 14:
            temp[1].append(mat[nx][ny + i])
    for i in range(-4, 5):
        if 0 <= nx + i <= 14 and 0 <= ny + i <= 14:
            temp[2].append(mat[nx + i][ny + i])
    for i in range(-4, 5):
        if 0 <= nx + i <= 14 and 0 <= ny - i <= 14:
            temp[3].append(mat[nx + i][ny - i])

    for chess_list in temp:
        cnt = 0
        for now in chess_list:
            if now == turn:
                cnt += 1
            else:
                cnt = 0
            if cnt >= 5:
                return True
    return False


def ai(chess, temp, now_turn):
    ai_dll = cdll.LoadLibrary("E:/Chess/Python/Evolution/temp.dll")
    c_input = (c_int * 15 * 15)()
    for i in range(15):
        for j in range(15):
            c_input[i][j] = chess[i][j]
    ai_dll.begin_search(c_input, now_turn)
    for i in range(15):
        for j in range(15):
            if not chess[i][j] == c_input[i][j]:
                temp[0] = i
                temp[1] = j
                chess[i][j] = c_input[i][j]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(225, 300)
        self.fc2 = nn.Linear(300, 1)

    def forward(self, x):
        # 前向传播
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def choose(nets):
    global group_cnt
    fit_v = []
    sum = 0
    for i in range(group_cnt):
        v = fitness(nets[i], True if i == 0 else False)
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


def fitness(net, flag=False):
    chessboard = np.zeros((15, 15), dtype=int)
    chessboard[7][7] = 1
    now_turn = -1
    cnt = 0
    while True:
        temp = [0, 0]
        ai(chessboard, temp, now_turn)
        if check(temp[0], temp[1], chessboard, now_turn):
            break
        now_turn = -now_turn
        max_v = -1e9
        index = -1
        for i in range(15):
            for j in range(15):
                if chessboard[i][j] == 0:
                    chessboard[i][j] = now_turn
                    x = torch.from_numpy(chessboard)
                    x = x.view(-1, num_flat_features(x))
                    x = x.float()
                    out = net(x)
                    out = float(out)
                    if max_v < out:
                        max_v = out
                        index = i * 15 + j
                    chessboard[i][j] = 0
        i = index // 15
        j = index % 15
        chessboard[i][j] = now_turn
        if check(i, j, chessboard, now_turn):
            cnt += 1000
            break
        now_turn = -now_turn
        cnt += 2
        if flag:
            print(chessboard)
    return cnt


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
    s = np.random.randint(0, par_maxcnt - 2)
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
                            param[i][j] = np.random.random()
                        cnt += 1
            elif 'bias' in name:
                for i in range(param.size()[0]):
                    param[i] = np.random.random()
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


group_cnt = 10
cross_p = 0.88
mutation_p = 0.01
epochs = 100

temp_net = Net()
par_maxcnt = sum(p.numel() for p in temp_net.parameters() if p.requires_grad)

net_group = [Net() for i in range(group_cnt)]

for i in range(epochs):
    s = time.time()
    evolution(net_group)
    e = time.time()
    print("cost", e - s, "s")
