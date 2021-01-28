import copy
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
        self.fc2 = nn.Linear(300, 225)

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
        v = fitness(nets[i])
        fit_v.append(v)
        sum += v

    for i in range(group_cnt):
        fit_v[i] /= sum

    choose_index = []
    for i in range(group_cnt):
        choose_index.append(np.random.choice(range(group_cnt), p=fit_v))

    res = []
    for i in choose_index:
        res.append(copy.deepcopy(nets[i]))

    return res


def fitness(net):
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
        x = torch.from_numpy(chessboard)
        x = x.view(-1, num_flat_features(x))
        x = x.float()
        out = net(x)
        index = torch.max(out, dim=1)[1]
        i = index // 15
        j = index % 15
        chessboard[i][j] = now_turn
        if check(temp[0], temp[1], chessboard, now_turn):
            cnt += 1000
            break
        now_turn = -now_turn
        cnt += 2
        print(chessboard)

    return cnt


def cross(net1, net2):
    pass

def mutation(net1):
    pass


group_cnt = 10
temp_net = Net()
par_maxcnt = sum(p.numel() for p in temp_net.parameters() if p.requires_grad)

net_group = [Net() for i in range(group_cnt)]
