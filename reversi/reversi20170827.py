#黑白棋
#根据书上程序，结合苹果手机里的一款黑白棋游戏，进行修改

import pygame,sys,time

class Reversi:
    def __init__(self):
        self.start_piece=-1        # 初始棋子，即谁先走
        self.board=[]              # 棋盘(二维列表)
        self.currten_piece=-1      # 当前下棋的棋子颜色
        self.enabalemove=False     # 当前棋子有没有合法的落子点，如果没有就需要通过成绩比较判断输赢
        self.pointlist=[]          # 如果有合法落子点，则记录所有的位置坐标的列表(二维列表)
        self.reverslist=[]         # 每个合法落子所对应的可翻转的对方棋子的坐标列表(二维列表)
        self.round=0               # 第几局比赛
        self.roundscore=[0,0]      # 大比分
        self.score = [0,0]         # 当前局比分
        self.step=0                # 当前局步数
        self.record=[]             # 棋谱记录.undo可以通过棋谱从第一步开始计算的形式，以计算时间换取存储空间(二维列表)

        self.resetBoard()

    def clearlist(self,l):
        #清空列表
        while l:
            l.pop()
        return l

    def resetBoard(self):
        # 游戏数据清零,每个玩家有两个棋子在棋盘的中央
        # 用于开始新游戏
        for i in range(8):
            self.board.append([0] * 8)
        self.board[3][3] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = -1

        self.pointlist = []
        self.reverslist = []
        self.roundscore = [0, 0]
        self.score = [0, 0]
        self.step = 0
        self.record = []

    def isOnBoard(x, y):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            return True
        else:
            return False

    def judge_point(self, piece, pos):
        # 在棋盘上根据在行列pos[row,col]上的落子piece，计算可以被翻转的对方棋子，
        # 如果有棋子可以翻转，则返回棋子坐标的列表。否则返回False
        dir = [[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]]

        reverlist = []  # 八个方向的总列表
        # 八个方向遍历
        for i in range(8):
            revli = []  # 一个方向的小列表
            r, c = pos
            while True:
                r += dir[i][1]
                c += dir[i][0]
                if self.isOnBoard(r, c):
                    if self.board[r][c] == -piece:
                        # 只有遇到对方棋子，就在小列表中记录其坐标
                        revli.append([r, c])
                    elif self.board[r][c] == piece:
                        # 遇到同色棋子，把小列表并入大列表，
                        # 退出while循环,进入下一个方向的判断
                        for rr, cc in revli:
                            reverlist.append([rr, cc])
                        break
                    elif self.board[r][c] == 0 or self.board[r][c] >= 100:
                        # 遇到空白则退出whie循环，进入下一个方向的判断
                        break
                else:
                    # 超出棋盘的范围
                    break
        if len(reverlist) == 0:
            return False
        return reverlist

    def judge_all(self, piece):
        # 判断当前棋子的所有可能的落子点
        # 落子点坐标存在pointlist列表中
        # 每个落子点对应的可以翻转的对方棋子的坐标存在reverslist列表中
        self.pointlist=[[],[]]

        # 清理辅助棋子数据
        for r in range(8):
            for c in range(8):
                if self.board[r][c] >= 100:
                    self.board[r][c] = 0
        # 开始遍历所有空白棋格
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 0 or self.board[r][c]>=100:
                    revlst = self.judge_point(piece, [r, c])
                    if revlst == False:
                        # 该位置不能落子，开始下一个for循环
                        continue
                    else:
                        # 在复制的数据里记录位置数据
                        self.board[r][c] = 100 + len(revlst)
                        self.pointlist.append([r,c])
                        self.reverslist.append(revlst)

    def computermove(self):
        #根据judgeall函数的结果，查找最优落子点的位置
        #本方法很简单，就是根据翻转棋子的数量进行判断，没有考虑特殊点等一些情况
        #后期可以进行扩展
        maxrow = -1
        maxcol = -1
        maxpiece = 101  # 最小值为101-100
        #遍历所有合法点
        for r,c in self.pointlist:
            if self.board[r][c] >= maxpiece:  # 必须是>=
                maxrow = r
                maxcol = c
                maxpiece = board[r][c]

        return maxrow, maxcol

    def





