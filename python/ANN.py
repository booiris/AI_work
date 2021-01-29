import copy
import random
from ctypes import *

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


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

    # index = []
    # for i in range(15):
    #     for j in range(15):
    #         if chess[i][j] == 0:
    #             index.append([i, j])
    # p = random.randint(0, len(index) - 1)
    # chess[index[p][0]][index[p][1]] = now_turn
    # temp[0] = index[p][0]
    # temp[1] = index[p][1]

    global net, now_index
    action, q_value = cal_q_value(net, chess, now_turn, steps[now_index][2:6])
    index = q_value.index(max(q_value))
    temp[0] = action[index][0]
    temp[1] = action[index][1]


maxsize = 300
epochs = 1
now_index = 1
batch_size = 32
now_turn = -1
renew_max = 40
sita = 0.1

value = np.empty([15, 15])
p = 0
q = 14
t = 0
while p < q:
    for i in range(p, q):
        value[p][i] = t
    for i in range(p, q):
        value[i][q] = t
    for i in range(q, p, -1):
        value[q][i] = t
    for i in range(q, p, -1):
        value[i][p] = t
    t += 0.01
    p += 1
    q -= 1
if q == p:
    value[p][p] = t

chessboard = np.empty([15, 15], dtype=int)
now_state = np.empty([maxsize, 15, 15], dtype=int)
reward = np.empty([maxsize, 3])  # 0 reward 1是否结束 2是否是开始
steps = np.empty([maxsize, 8], dtype=int)  # 0,1 ai上一步下的，2,3 对手上一步下的, 4,5 ai这一步下的, 6,7 对手这一步下的
steps[0][0:8] = -1


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
    steps[now_index][0] = steps[now_index - 1][4]
    steps[now_index][1] = steps[now_index - 1][5]
    steps[now_index][2] = steps[now_index - 1][6]
    steps[now_index][3] = steps[now_index - 1][7]
    steps[now_index][4] = x
    steps[now_index][5] = y
    steps[now_index][6] = -1
    steps[now_index][7] = -1
    if check(x, y, chess, now_turn):
        reward[now_index][1] = 1
        return 1
    temp = [0, 0]
    ai(chess, temp, -now_turn)
    steps[now_index][6] = temp[0]
    steps[now_index][7] = temp[1]
    if check(temp[0], temp[1], chess, -now_turn):
        reward[now_index][1] = -1
        return -1
    reward[now_index][1] = 0
    return 0


def cal_q_value(net, chessboard, now_turn, step):
    action = []
    q_value = []
    for i in range(15):
        for j in range(15):
            if chessboard[i][j] == 0:
                x = torch.empty(1, 4, 15, 15)
                if step[0] < 0:
                    x[0][0] = copy.deepcopy(torch.from_numpy(chessboard))
                    x[0][1] = copy.deepcopy(torch.from_numpy(chessboard))
                    x[0][2] = copy.deepcopy(torch.from_numpy(chessboard))
                else:
                    chessboard[step[0]][step[1]] = 0
                    chessboard[step[2]][step[3]] = 0
                    x[0][0] = copy.deepcopy(torch.from_numpy(chessboard))
                    chessboard[step[0]][step[1]] = now_turn
                    x[0][1] = copy.deepcopy(torch.from_numpy(chessboard))
                    chessboard[step[2]][step[3]] = -now_turn
                    x[0][2] = copy.deepcopy(torch.from_numpy(chessboard))
                chessboard[i][j] = now_turn
                x[0][3] = copy.deepcopy(torch.from_numpy(chessboard))
                action.append([i, j])
                with torch.no_grad():
                    out = net(x)
                q_value.append(float(out))
                chessboard[i][j] = 0

    return action, q_value


def build_data(net, now_turn, is_begin):
    global now_index
    if is_begin:
        reward[now_index][2] = 1
        step = [-1, -1, -1, -1]
    else:
        reward[now_index][2] = 0
        step = steps[now_index - 1][4:8]
    action, q_value = cal_q_value(net, chessboard, now_turn, step)
    p = random.random()
    if p < sita or max(q_value) - min(q_value) == 0:
        index = random.randint(0, len(action) - 1)
    else:
        index = q_value.index(max(q_value))
    chessboard[action[index][0]][action[index][1]] = now_turn
    now_state[now_index] = copy.deepcopy(chessboard)

    nxt_reward = cal_reward(action[index][0], action[index][1], chessboard, now_turn, now_index)
    reward[now_index][0] = nxt_reward
    now_index += 1
    # print(chessboard)
    # print(q_value[0:5])
    # print(max(q_value), now_turn, action[index][0], action[index][1], nxt_reward)
    # if now_index % 100 == 0:
    #     print(chessboard)
    #     print(q_value[0:5], max(q_value), action[q_value.index(max(q_value))][0],
    #           action[q_value.index(max(q_value))][1])
    if reward[now_index - 1][1] != 0:
        return False
    else:
        return True


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, 6)  # 第一个卷积层，32个卷积核，大小为6x6
        self.conv2 = nn.Conv2d(32, 64, 5)  # 第二个卷积层，64个卷积核，大小为5x5
        self.conv3 = nn.Conv2d(64, 128, 4)  # 第三个卷积层，128个卷积核，大小为4x4
        self.fc1 = nn.Linear(128 * 3 * 3, 512)  # 第一个全连接层，输入为128*3*3,输出大小为512
        self.fc2 = nn.Linear(512, 128)  # 第二个全连接层，输入大小为512,输出大小为128
        self.fc3 = nn.Linear(128, 1)  # 第三个全连接层，输入大小为128,输出大小为1 即计算的Q值

    def forward(self, x):
        x = x.cuda()
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
    renew_cnt = 0
    is_begin = True
    global now_index, now_turn
    now_index = 1
    for k in range(15):
        for l in range(15):
            chessboard[k][l] = 0
    now_turn = 1
    for step in range(maxsize - 10):
        if not build_data(net, now_turn, is_begin):
            is_begin = True
            for m in range(15):
                for n in range(15):
                    chessboard[m][n] = 0
        else:
            is_begin = False
        if step > 80:
            data_index = random.sample(range(1, now_index), batch_size)
            random.shuffle(data_index)
            input = torch.empty([batch_size, 4, 15, 15])
            target = torch.empty([batch_size, 1])
            now_ini = 0
            for i in data_index:
                target[now_ini][0] = reward[i][0]
                if steps[i][0] < 0:
                    input[now_ini][0] = copy.deepcopy(torch.from_numpy(now_state[i]))
                    input[now_ini][1] = copy.deepcopy(torch.from_numpy(now_state[i]))
                    input[now_ini][2] = copy.deepcopy(torch.from_numpy(now_state[i]))
                else:
                    now_state[i][steps[i][0]][steps[i][1]] = 0
                    now_state[i][steps[i][2]][steps[i][3]] = 0
                    now_state[i][steps[i][4]][steps[i][5]] = 0
                    input[now_ini][0] = copy.deepcopy(torch.from_numpy(now_state[i]))
                    now_state[i][steps[i][0]][steps[i][1]] = now_turn
                    input[now_ini][1] = copy.deepcopy(torch.from_numpy(now_state[i]))
                    now_state[i][steps[i][2]][steps[i][3]] = -now_turn
                    input[now_ini][2] = copy.deepcopy(torch.from_numpy(now_state[i]))

                now_state[i][steps[i][4]][steps[i][5]] = now_turn
                input[now_ini][3] = copy.deepcopy(torch.from_numpy(now_state[i]))

                now_ini += 1

            now_ini = 0
            out = net(input)
            for i in data_index:
                temp_chessboard = now_state[i]
                if reward[i][1] != 0:
                    now_ini += 1
                    continue
                temp_chessboard[steps[i][6]][steps[i][7]] = -now_turn
                if reward[i][2] == 1:
                    step = [-1, -1, -1, -1]
                else:
                    step = steps[now_index - 1][4:8]
                action, q_value = cal_q_value(target_net, temp_chessboard, now_turn, step)
                temp_chessboard[steps[i][6]][steps[i][7]] = 0
                target[now_ini][0] += max(q_value)
                now_ini += 1

            target = target.cuda()
            loss = criterion(out, target)
            net.zero_grad()
            loss.backward()
            optimizer.step()
            renew_cnt += 1

            if renew_cnt > renew_max:
                wf = copy.deepcopy(net.state_dict())
                target_net.load_state_dict(wf)
                renew_cnt = 0
            print(torch.mean(loss))

    torch.save({
        'epoch': epochs,
        'model_state_dict': net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, "weight/temp.pth.tar")


def predict(chess, now_turn, net):
    action, q_value = cal_q_value(net, chess, now_turn)
    index = q_value.index(max(q_value))
    chess[action[index][0]][action[index][1]] = now_turn


net = Net()
target_net = Net()
net = net.cuda()
target_net = target_net.cuda()
optimizer = optim.Adam(net.parameters(), lr=0.001)

# checkpoint = torch.load("weight/ann.pth.tar")
# net.load_state_dict(checkpoint['model_state_dict'])
# optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
wf = copy.deepcopy(net.state_dict())
target_net.load_state_dict(wf)

# for i in range(15):
#     for j in range(15):
#         chessboard[i][j] = 0
# while 1:
#     x, y = input().split()
#     chessboard[int(x)][int(y)] = 1
#     predict(chessboard, -1, net)
#     print(chessboard)

criterion = nn.MSELoss()

for i in range(epochs):
    train()
    torch.save({
        'epoch': epochs,
        'model_state_dict': net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, "weight/ann.pth.tar")
