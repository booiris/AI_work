from tkinter import *

TAG_BLACK = 1
TAG_EMPTY = 0
TAG_WHITE = -1


class chess(object):
    def __init__(self):
        self.row, self.column = 15, 15
        self.is_star = True
        self.mesh = 40
        self.board_color = "#CDBA96"
        self.header_bg = "#CDC0B0"
        self.matrix = [[TAG_EMPTY for y in range(self.column)] for x in range(self.row)]
        self.now_turn = TAG_BLACK

        self.root = Tk()
        self.root.title("五子棋界面")
        self.root.geometry("900x640")
        self.root.resizable(width=False, height=False)

        self.chessboard = Canvas(self.root, bg="#CDBA96", width=(self.column + 1) * self.mesh,
                                 height=(self.row + 1) * self.mesh, highlightthickness=0)
        self.chessboard.pack(side=LEFT)
        self.draw_window()
        self.root.mainloop()

    def draw_window(self):
        self.chessboard.bind("<Button-1>", self.click)
        self.restar()

    def restar(self):
        self.draw_board()
        self.matrix = [[TAG_EMPTY for y in range(self.column)] for x in range(self.row)]
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
        if distance > self.mesh * 0.45 or self.matrix[x][y] != TAG_EMPTY or not self.is_star:
            return
        self.matrix[x][y] = self.now_turn
        self.draw_chess(x, y, self.now_turn)
        if self.check(x, y, self.now_turn):
            text = "黑胜" if self.now_turn > 0 else "白胜"
            self.center_show(text)
            self.is_star = False
            # self.restar()

        self.now_turn = -self.now_turn

    def center_show(self, text):
        width, height = int(self.chessboard['width']), int(self.chessboard['height'])
        self.chessboard.create_text(int(width / 2), int(height / 2), text=text, font=("黑体", 50, "bold"), fill="red")

    def draw_chess(self, x, y, now_turn):
        xx, yy = self.mesh * (x + 1), self.mesh * (y + 1)
        if now_turn > 0:
            color = "black"
        else:
            color = "white"
        self.chessboard.create_oval(yy - self.mesh * 0.3, xx - self.mesh * 0.3,
                                    yy + self.mesh * 0.3, xx + self.mesh * 0.3,
                                    fill=color)

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


chess()
