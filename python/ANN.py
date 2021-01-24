import random
from ctypes import *

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


def ai(chess, temp, now_turn):
    ai_dll = cdll.LoadLibrary("E:/Chess/Python/temp.dll")
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


maxsize = 400
epochs = 2
now_index = 0
batch_size = 128
now_turn = -1

chessboard = np.empty([15, 15], dtype=int)
now_state = np.empty([maxsize, 15, 15], dtype=int)
reward = np.empty([maxsize, 4])


def num_flat_features(x):  # 计算矩阵特征数
    size = x.size()[1:]
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


def cal_reward(x, y, chess, now_turn, now_index):
    chess[x][y] = now_turn
    if check(x, y, chess, now_turn):
        reward[now_index][3] = 1
        return 1000
    temp = [0, 0]
    ai(chess, temp, -now_turn)
    reward[now_index][1] = temp[0]
    reward[now_index][2] = temp[1]
    if check(temp[0], temp[1], chess, -now_turn):
        reward[now_index][3] = -1
        return -1000
    reward[now_index][3] = 0
    return 0


def cal_q_value(net, chessboard, now_turn):
    action = []
    p = []
    q_value = []
    sum = 0.0
    for i in range(15):
        for j in range(15):
            if chessboard[i][j] == 0:
                chessboard[i][j] = now_turn
                action.append([i, j])
                x = torch.from_numpy(chessboard)
                x = x.unsqueeze(0)
                x = x.unsqueeze(1)
                x = x.float()
                with torch.no_grad():
                    out = net(x)
                p.append(float(out))
                q_value.append(float(out))
                chessboard[i][j] = 0

    maxp = max(p)
    minp = min(p)
    if maxp - minp == 0:
        for i in range(len(p)):
            p[i] = 1 / len(p)
    else:
        for i in range(len(p)):
            p[i] = (p[i] - minp) / (maxp - minp)
            sum += p[i]
        for i in range(len(p)):
            p[i] = p[i] / sum

    return action, p, q_value


def build_data(net, now_turn):
    global now_index
    action, p, _ = cal_q_value(net, chessboard, now_turn)
    index = np.random.choice(range(len(action)), p=p)
    chessboard[action[index][0]][action[index][1]] = now_turn
    for i in range(15):
        for j in range(15):
            now_state[now_index][i][j] = chessboard[i][j]

    nxt_reward = cal_reward(action[index][0], action[index][1], chessboard, now_turn, now_index)
    reward[now_index][0] = nxt_reward
    now_index += 1
    if now_index % 20 == 0:
        print(chessboard)
    if nxt_reward != 0:
        return False
    else:
        return True


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 6)  # 第一个卷积层，32个卷积核，大小为6x6
        self.conv2 = nn.Conv2d(32, 64, 5)  # 第二个卷积层，64个卷积核，大小为5x5
        self.conv3 = nn.Conv2d(64, 128, 4)  # 第三个卷积层，128个卷积核，大小为4x4
        self.fc1 = nn.Linear(128 * 3 * 3, 512)  # 第一个全连接层，输入为128*3*3,输出大小为512
        self.fc2 = nn.Linear(512, 128)  # 第二个全连接层，输入大小为512,输出大小为128
        self.fc3 = nn.Linear(128, 1)  # 第三个全连接层，输入大小为128,输出大小为1 即计算的Q值

    def forward(self, x):
        # 前向传播
        x = F.relu(self.conv1(x))  # 第一个卷积层计算
        x = F.relu(self.conv2(x))  # 第二个卷积层计算
        x = F.relu(self.conv3(x))  # 第三个卷积层计算
        x = x.view(-1, num_flat_features(x))  # 原来矩阵转换为一维向量输入全连接层
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train():
    global now_index
    now_index = 0
    for k in range(15):
        for l in range(15):
            chessboard[k][l] = 0
    while now_index < maxsize:
        chessboard[7][7] = 1
        for i in range(112):
            if (not build_data(net, now_turn)) or now_index >= maxsize:
                for k in range(15):
                    for l in range(15):
                        chessboard[k][l] = 0
                break
    data_index = random.sample(range(maxsize), batch_size)
    random.shuffle(data_index)
    input = torch.empty([batch_size, 1, 15, 15])
    target = torch.empty([batch_size, 1])
    now_ini = 0
    for i in data_index:
        target[now_ini][0] = reward[i][0]
        input[now_ini][0] = torch.from_numpy(now_state[i])
        now_ini += 1

    now_ini = 0
    out = net(input)
    for i in data_index:
        temp_chessboard = now_state[i]
        if (reward[i][3] != 0):
            now_ini += 1
            continue
        temp_chessboard[int(reward[i][1])][int(reward[i][2])] = -now_turn
        action, p, q_value = cal_q_value(net, temp_chessboard, now_turn)
        target[now_ini][0] += max(q_value)
        now_ini += 1

    loss = criterion(out, target)
    print(torch.mean(loss))
    net.zero_grad()
    loss.backward()
    optimizer.step()

net = Net()
optimizer = optim.Adam(net.parameters(), lr=0.01)


# checkpoint = torch.load("weight/temp.pth.tar")
# net.load_state_dict(checkpoint['model_state_dict'])
# optimizer.load_state_dict(checkpoint['optimizer_state_dict'])


criterion = nn.MSELoss()


for i in range(epochs):
    train()
torch.save({
     'epoch': epochs,
     'model_state_dict': net.staet_dict(),
     'optimizer_state_dict': optimizer.state_dict(),
 }, "weight/temp.pth.tar")
