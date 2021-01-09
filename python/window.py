import ctypes
import time
from tkinter import *

from PIL import ImageGrab

from C_AI import ai

TAG_BLACK = 1
TAG_EMPTY = 0
TAG_WHITE = -1

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)


class chess(object):
    def __init__(self):
        self.row, self.column = 15, 15
        self.ai_working = False
        self.is_star = True
        self.mesh = 40
        self.board_color = "#CDBA96"
        self.header_bg = "#CDC0B0"
        self.matrix = [[TAG_EMPTY for y in range(self.column)] for x in range(self.row)]
        self.now_turn = TAG_BLACK

        self.root = Tk()
        self.root.tk.call('tk', 'scaling', ScaleFactor / 75)
        self.root.title("五子棋界面")
        self.root.geometry("900x640+500+100")
        self.root.resizable(width=False, height=False)

        self.chessboard = Canvas(self.root, bg="#CDBA96", width=(self.column + 1) * self.mesh,
                                 height=(self.row + 1) * self.mesh, highlightthickness=0)
        self.chessboard.pack(side=LEFT)
        # self.restar()
        # self.root.mainloop()

    def screen_shot(self, filename):
        self.root.update()
        x = self.root.winfo_x() + self.chessboard.winfo_x() + 10
        y = self.root.winfo_y() + self.chessboard.winfo_y() + 40
        x1 = x + self.chessboard.winfo_width()
        y1 = y + self.chessboard.winfo_height()
        time.sleep(0.3)
        ImageGrab.grab().crop((x, y, x1, y1)).save(filename)

    def draw_window(self):
        self.chessboard.bind("<Button-1>", self.click)
        self.restar()
        self.root.mainloop()

    def restar(self):
        self.matrix = [[TAG_EMPTY for y in range(self.column)] for x in range(self.row)]
        self.draw_board()
        self.chessboard.update()
        self.now_turn = TAG_BLACK
        self.is_star = True

    def draw_board(self):
        for x in range(self.row - 1):
            for y in range(self.column - 1):
                self.draw_mesh(x, y)

    def draw_mesh(self, x, y):
        xx, yy = x * self.mesh + self.mesh, y * self.mesh + self.mesh
        self.chessboard.create_rectangle(xx, yy, xx + self.mesh, yy + self.mesh, fill=self.board_color, outline="black")

        if ((x == 3 or x == 11) and (y == 3 or y == 11)) or (x == 7 and y == 7):
            self.chessboard.create_oval(xx - 0.085 * self.mesh, yy - 0.085 * self.mesh,
                                        xx + 0.085 * self.mesh, yy + 0.085 * self.mesh,
                                        fill="#000")

    def click(self, e):
        x, y = round((e.y - self.mesh) / self.mesh), round((e.x - self.mesh) / self.mesh)
        xx, yy = self.mesh * (x + 1), self.mesh * (y + 1)
        distance = ((xx - e.y) ** 2 + (yy - e.x) ** 2) ** 0.5
        if distance > self.mesh * 0.45 or self.matrix[x][y] != TAG_EMPTY or not self.is_star or self.ai_working:
            return
        self.matrix[x][y] = self.now_turn
        self.draw_chess()
        if self.check(x, y, self.now_turn):
            text = "黑胜" if self.now_turn > 0 else "白胜"
            self.center_show(text)
            self.is_star = False
            self.restar()
            return
        self.chessboard.update()

        self.now_turn = -self.now_turn
        self.ai_working = True
        temp = [x, y]
        ai(self, temp)

        x = temp[0]
        y = temp[1]
        self.draw_chess()
        if self.check(x, y, self.now_turn):
            text = "黑胜" if self.now_turn > 0 else "白胜"
            self.center_show(text)
            self.is_star = False
            self.restar()
            return
        self.ai_working = False
        self.now_turn = -self.now_turn

    def center_show(self, text):
        width, height = int(self.chessboard['width']), int(self.chessboard['height'])
        print(width, height, text)
        self.chessboard.create_text(int(width / 2), int(height / 2), text=text, font=("黑体", 50, "bold"), fill="red")
        self.chessboard.update()
        time.sleep(1)

    def draw_chess(self):
        self.chessboard.delete("chess")
        for x in range(self.row):
            for y in range(self.column):
                xx, yy = self.mesh * (x + 1), self.mesh * (y + 1)
                if self.matrix[x][y] == TAG_EMPTY:
                    continue
                if self.matrix[x][y] == TAG_BLACK:
                    color = "black"
                if self.matrix[x][y] == TAG_WHITE:
                    color = "white"
                self.chessboard.create_oval(yy - self.mesh * 0.3, xx - self.mesh * 0.3,
                                            yy + self.mesh * 0.3, xx + self.mesh * 0.3,
                                            fill=color, tag="chess")

    def check(self, x, y, now_turn):
        temp = [[] for _ in range(4)]
        for i in range(-4, 5):
            if 0 <= x + i <= 14:
                temp[0].append(self.matrix[x + i][y])
        for i in range(-4, 5):
            if 0 <= y + i <= 14:
                temp[1].append(self.matrix[x][y + i])
        for i in range(-4, 5):
            if 0 <= x + i <= 14 and 0 <= y + i <= 14:
                temp[2].append(self.matrix[x + i][y + i])
        for i in range(-4, 5):
            if 0 <= x + i <= 14 and 0 <= y - i <= 14:
                temp[3].append(self.matrix[x + i][y - i])

        for chess_list in temp:
            cnt = 0
            for now in chess_list:
                if now == now_turn:
                    cnt += 1
                else:
                    cnt = 0
                if cnt >= 5:
                    return True
        return False
