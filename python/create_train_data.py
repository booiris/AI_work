import random

from window import chess

chess = chess()
chess.restar()
now_turn = 1
for i in range(100):
    while True:
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        if chess.matrix[x][y] == 0:
            break
    chess.matrix[x][y] = now_turn
    chess.draw_chess()
    now_turn = -now_turn
chess.root.mainloop()

# maxnum = 200
# chess_list = [[] for i in range(maxnum)]
# chess = chess()
# is_begin = False
# now_turn = 1
# for i in range(maxnum):
#     print(i)
#     if not is_begin or i % 75 == 0:
#         chess.restar()
#         chess_list.clear()
#         is_begin = True
#         now_turn = 1
#     filename = "chess/images/" + str(i) + ".jpg"
#     labelname = "chess/labels/" + str(i) + ".txt"
#
#     while True:
#         x = random.randint(0, 14)
#         y = random.randint(0, 14)
#         if chess.matrix[x][y] == 0:
#             break
#
#     chess.matrix[x][y] = now_turn
#     xx, yy = chess.mesh * (x + 1), chess.mesh * (y + 1)
#     chess_list.append([0 if now_turn == 1 else 1, yy / 640, xx / 640, 0.0453125, 0.0453125])
#     with open(labelname, "w+", encoding='utf-8')as f:
#         line = ""
#         for k in chess_list:
#             for j in k:
#                 line += str(j) + ' '
#             line += '\n'
#         f.writelines(line)
#
#     chess.draw_chess()
#     if chess.check(x, y, now_turn):
#         text = "黑胜" if now_turn > 0 else "白胜"
#         is_begin = False
#     now_turn = -now_turn
#     chess.root.after(1, chess.screen_shot(filename))
#     chess.root.after(400, chess.root.quit)
#     chess.root.mainloop()
#     time.sleep(0.4)
# chess.root.after(1, chess.root.destroy)
# chess.root.mainloop()
