from ctypes import *


def ai(chess, temp):
    ai_dll = cdll.LoadLibrary("temp.dll")
    c_input = (c_int * 15 * 15)()
    for i in range(15):
        for j in range(15):
            c_input[i][j] = chess.matrix[i][j]
    ai_dll.begin_search(c_input, chess.now_turn)
    for i in range(15):
        for j in range(15):
            if not chess.matrix[i][j] == c_input[i][j]:
                temp[0] = i
                temp[1] = j
                chess.matrix[i][j] = c_input[i][j]

# chess = chess()
# ai(chess)
