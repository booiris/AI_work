import copy
import random
import time
from ctypes import *

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


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


def change(step, chessboard, now_turn):
    x = torch.empty(1, 4, 15, 15)
    if step[0][0] > 0:
        chessboard[step[0][0]][step[0][1]] = 0
    if step[1][0] > 0:
        chessboard[step[1][0]][step[1][1]] = 0
    x[0][0] = copy.deepcopy(torch.from_numpy(chessboard))
    if step[0][0] > 0:
        chessboard[step[0][0]][step[0][1]] = now_turn
    x[0][1] = copy.deepcopy(torch.from_numpy(chessboard))
    if step[1][0] > 0:
        chessboard[step[1][0]][step[1][1]] = -now_turn
    x[0][2] = copy.deepcopy(torch.from_numpy(chessboard))
    chessboard[step[2][0]][step[2][1]] = now_turn
    x[0][3] = copy.deepcopy(torch.from_numpy(chessboard))
    chessboard[step[2][0]][step[2][1]] = 0
    return x


def cal_q_value(now_net, chessboard, now_turn, steps_index, steps):
    action = []
    q_value = []
    for i in range(15):
        for j in range(15):
            if chessboard[i][j] == 0:
                step = []
                step.append([-1, -1] if steps_index < 2 else steps[steps_index - 2])
                step.append([-1, -1] if steps_index < 1 else steps[steps_index - 1])
                step.append([i, j])
                x = change(step, chessboard, now_turn)
                action.append([i, j])
                with torch.no_grad():
                    out = now_net(x)
                q_value.append(float(out))

    return action, q_value


def ai(chess, temp, now_turn):
    ai_dll = cdll.LoadLibrary("E:/Chess/Python/temp.dll")
    # c_input = (c_int * 15 * 15)()
    # for i in range(15):
    #     for j in range(15):
    #         c_input[i][j] = chess[i][j]
    # ai_dll.begin_search(c_input, now_turn)
    # for i in range(15):
    #     for j in range(15):
    #         if not chess[i][j] == c_input[i][j]:
    #             temp[0] = i
    #             temp[1] = j
    #             chess[i][j] = c_input[i][j]
    index = []
    for i in range(15):
        for j in range(15):
            if chess[i][j] == 0:
                index.append([i, j])
    p = random.randint(0, len(index) - 1)
    chess[index[p][0]][index[p][1]] = now_turn
    temp[0] = index[p][0]
    temp[1] = index[p][1]


def build_data(net, chessboard):
    now_turn = 1
    global now_index
    star_index = now_index
    for i in range(225):
        reward[now_index][2] = now_turn
        reward[now_index][3] = star_index
        action, q_value = cal_q_value(net, chessboard, now_turn, now_index, steps)

        p = random.random()
        if p < sita or max(q_value) - min(q_value) == 0:
            index = random.randint(0, len(action) - 1)
        else:
            index = q_value.index(max(q_value))
        nx = action[index][0]
        ny = action[index][1]
        steps.append([nx, ny])
        chessboard[nx][ny] = now_turn
        now_state[now_index] = copy.deepcopy(chessboard)

        if check(nx, ny, chessboard, now_turn):
            reward[now_index][1] = 1
            now_index += 1
            break
        else:
            reward[now_index][1] = 0
            now_turn = -now_turn
            now_index += 1

        print(chessboard)
        print(q_value[0:5])
        print(now_index, max(q_value), now_turn, nx, ny)

        temp = [0, 0]
        reward[now_index][2] = now_turn
        reward[now_index][3] = star_index
        ai(chessboard, temp, now_turn)
        steps.append([temp[0], temp[1]])
        now_state[now_index] = copy.deepcopy(chessboard)
        if check(temp[0], temp[1], chessboard, now_turn):
            reward[now_index][1] = 1
            now_index += 1
            break
        else:
            reward[now_index][1] = 0
            now_turn = -now_turn
            now_index += 1

    end_index = now_index
    # 计算reward
    n_index = copy.deepcopy(now_index)
    n_index -= 1
    winner = now_turn
    while n_index >= star_index:
        if int(reward[n_index][2]) == winner:
            reward[n_index][0] = 1
        else:
            reward[n_index][0] = -(end_index - star_index) * np.power(0.9, end_index - n_index)
        n_index -= 1


def init():
    for i in range(15):
        for j in range(15):
            chessboard[i][j] = 0
    steps.clear()


def train(net, target_net, chessboard):
    global now_index
    now_index = 0
    init()
    while now_index < index_max:
        for i in range(15):
            for j in range(15):
                chessboard[i][j] = 0
        build_data(net, chessboard)

    index = []
    for i in range(now_index):
        if reward[i][2] == 1:
            index.append(i)
    data_index = random.sample(index, batch_size)
    random.shuffle(data_index)
    target = torch.empty([batch_size, 1])
    now_ini = 0
    input = torch.empty([batch_size, 4, 15, 15])
    for i in data_index:
        target[now_ini][0] = reward[i][0]
        step = []
        steps_index = i - reward[i][3]
        step.append([-1, -1] if steps_index < 2 else steps[i - 2])
        step.append([-1, -1] if steps_index < 1 else steps[i - 1])
        step.append(steps[i])
        input[now_ini] = change(step, now_state[i], reward[i][2])
        now_ini += 1

    now_ini = 0
    out = net(input)
    for i in data_index:
        if reward[i][1] == 1:
            now_ini += 1
            continue
        action, q_value = cal_q_value(target_net, now_state[i + 1], int(reward[i][2]), int(i + 1 - reward[i][3]),
                                      steps[int(reward[i + 1][3]):])
        target[now_ini][0] += max(q_value)
        now_ini += 1
    target = target.cuda()
    loss = criterion(out, target)
    net.zero_grad()
    loss.backward()
    optimizer.step()
    print(torch.mean(loss))


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, 6)  # 第一个卷积层，32个卷积核，大小为6x6
        self.conv2 = nn.Conv2d(32, 64, 5)  # 第二个卷积层，64个卷积核，大小为5x5
        self.fc1 = nn.Linear(64 * 6 * 6, 1024)  # 第一个全连接层，输入为128*3*3,输出大小为512
        self.fc2 = nn.Linear(1024, 512)  # 第二个全连接层，输入大小为512,输出大小为128
        self.fc3 = nn.Linear(512, 1)  # 第三个全连接层，输入大小为128,输出大小为1 即计算的Q值

    def forward(self, x):
        x = x.cuda()
        # 前向传播
        x = F.relu(self.conv1(x))  # 第一个卷积层计算
        x = F.relu(self.conv2(x))  # 第二个卷积层计算
        x = x.view(-1, num_flat_features(x))  # 原来矩阵转换为一维向量输入全连接层
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


index_max = 60
maxsize = 300
epochs = 300
now_index = 1
batch_size = 32
renew_max = 50
sita = 0.1

chessboard = np.empty([15, 15], dtype=int)
now_state = np.empty([maxsize, 15, 15], dtype=int)
reward = np.empty([maxsize, 4])  # 0 reward 1是否结束 2 表示当前下棋的人 3 开始局面的下标
steps = []

net = Net()
target_net = Net()
optimizer = optim.Adam(net.parameters(), lr=0.001)

wf = copy.deepcopy(net.state_dict())
target_net.load_state_dict(wf)
net = net.cuda()
target_net = target_net.cuda()

checkpoint = torch.load("weight/ai.pth.tar")
net.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

criterion = nn.MSELoss()

renew_cnt = 0
for i in range(epochs):
    time_start = time.time()
    print('epoch:', i)
    train(net, target_net, chessboard)
    renew_cnt += 1
    if renew_cnt > renew_max:
        wf = copy.deepcopy(net.state_dict())
        target_net.load_state_dict(wf)
        renew_cnt = 0
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    if i % 100 == 0:
        torch.save({
            'epoch': epochs,
            'model_state_dict': net.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, "weight/temp2.pth.tar")

torch.save({
    'epoch': epochs,
    'model_state_dict': net.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
}, "weight/temp2.pth.tar")
