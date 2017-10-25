# 黑白棋ver0.3
# 根据书上程序，结合苹果手机里的一款黑白棋游戏的界面和流程
# 采用面向对象的方法编程，将数据层和显示操作层分离，
# 优化了程序逻辑，主程序简洁明了
# 实现了动态显示棋子翻转过程，对整个显示的逻辑进行了重大的调整
# 完善了胜负判定,改进了提示框的显示(undo后可以显示当前棋),pass显示正确
# 待改进处：
# 一个底纹，根据选择进行合成，显示
# 当前棋子的动态显示



import pygame, sys, time


class Reversi:
    # 棋盘数据层
    # 棋盘(二维列表)-1黑棋，0空格，1白棋，>100则表示，针对当前颜色棋子，该位置是一种合理的落子点
    # 其值减去100所得结果，表示在改点落子后，可以翻转的对方棋子的数量
    def __init__(self, stpiece):
        self.people2machine = True
        self.start_piece = stpiece  # 初始棋子，即谁先走
        self.board = []  # 棋盘(二维列表)。-1黑棋，0空格，1白棋，>=100则表示改位置是一种合理的走棋点，
        self.current_piece = stpiece  # 当前下棋的棋子颜色
        self.player = ['people', 'computer']  # 黑棋与白棋对应的玩家（人或者电脑）
        self.enabalemove = [True, True]  # (黑与白)当前-- 有没有合法的落子点
        self.validpointlist = []  # 如果有合法落子点，则记录所有的位置坐标的列表(一维列表，每个元素是一个棋子坐标)
        self.reverslist = []  # 每个合法落子所对应的可翻转的对方棋子的坐标列表(二维列表，每个元素是一个列表)
        self.actual_revlst = []  # 最终选择的落子所对应的可翻转的对方棋子的坐标列表(一维列表，每个元素是一个棋子坐标)
        self.round = 0  # 第几局比赛
        self.roundscore = [0, 0]  # 大比分(黑比白)
        self.score = [0, 0]  # 当前局比分(黑比白)
        self.step = 0  # 当前局步数
        self.record = []  # 棋谱记录.undo可以通过棋谱从第一步开始计算的形式，以计算时间换取存储空间(一维列表)
        self.resetBoard(True)

    def clearList(self, l):
        # 清空列表
        while l:
            l.pop()
        return l

    def resetBoard(self, resetall=False):
        # 游戏数据清零,每个玩家有两个棋子在棋盘的中央
        # 用于开始新游戏
        # 需要增加考虑白棋先行的情况
        self.clearList(self.board)
        for i in range(8):
            self.board.append([0] * 8)
        self.board[3][3] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = -1
        self.current_piece = self.start_piece
        self.score = [2, 2]
        self.step = 0
        self.clearList(self.validpointlist)
        self.clearList(self.reverslist)
        self.clearList(self.actual_revlst)
        self.clearList(self.record)
        if resetall:
            self.roundscore = [0, 0]
            self.round = 0

        self.caculateAllPoint()

    def isOnBoard(self, x, y):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            return True
        else:
            return False

    def caculateOnePoint(self, pos):
        # 在棋盘上根据在行列pos[row,col]上的落子current_piece，计算可以被翻转的对方棋子，
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
                    if self.board[r][c] == -self.current_piece:
                        # 只有遇到对方棋子，就在小列表中记录其坐标
                        revli.append([r, c])
                    elif self.board[r][c] == self.current_piece:
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

    def caculateAllPoint(self):
        # 判断当前棋子current_piece的所有可能的落子点
        # 落子点坐标存在validpointlist列表中
        # 每个落子点对应的可以翻转的对方棋子的坐标存在reverslist列表中
        # 如果没有合法落子点(validpointlist列表为空)，则返回False。否则返回True
        self.clearList(self.validpointlist)
        self.clearList(self.reverslist)
        self.clearList(self.actual_revlst)

        # 清理辅助棋子数据
        for r in range(8):
            for c in range(8):
                if self.board[r][c] >= 100:
                    self.board[r][c] = 0
        # 开始遍历所有空白棋格
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 0:
                    revlst = self.caculateOnePoint([r, c])
                    if revlst == False:
                        # 该位置不能落子，开始下一个for循环
                        continue
                    else:
                        # 在复制的数据里记录位置数据
                        self.board[r][c] = 100 + len(revlst)
                        self.validpointlist.append([r, c])
                        self.reverslist.append(revlst)
        # 设置当前棋子有无合法落子点的标志
        p = self.current_piece  # 棋子颜色转变为enablemove[]的下标
        if p == -1:
            p = 0
        if len(self.validpointlist) == 0:
            self.enabalemove[p] = False  # 此语句及变量应该可以取消，后期调试看再优化
            return False
        else:
            self.enabalemove[p] = True  # 此语句及变量应该可以取消，后期调试看再优化
            return True

    def computerMove(self):
        # 根据judgeall函数的结果，查找最优落子点的位置
        # 本方法很简单，就是根据翻转棋子的数量进行判断，没有考虑特殊点等一些情况
        # 后期可以进行扩展
        maxrow = -1
        maxcol = -1
        maxpiece = 101  # 最小值为101-100
        # 遍历所有合法点
        for r, c in self.validpointlist:
            if self.board[r][c] >= maxpiece:  # 必须是>=
                maxrow = r
                maxcol = c
                maxpiece = self.board[r][c]

        return [maxrow, maxcol]

    def getScore(self):
        # 返回黑棋和白棋各自的数量
        bscore = 0
        wscore = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == -1:
                    bscore += 1
                elif self.board[r][c] == 1:
                    wscore += 1
        self.score = bscore, wscore

    def getActualRevlst(self, pos):
        # 计算玩家在合法落子点pos[row,col]处落子后，真正翻转的棋子序列
        #
        # 否则返回False
        if pos in self.validpointlist:
            # 当前位置是合法位置，可以落子
            p = self.validpointlist.index(pos)  # 取得当前位置在合法落子点列表中的序号
            for r, c in self.reverslist[p]:  # 取得翻转棋子的位置，开始翻转棋子
                self.actual_revlst.append([r, c])
            return True
        else:
            return False

    def addPiece(self, pos):
        # 在当前位置pos[row,col]处落子
        # pos=[-1,-1]，说明当前棋没有合理落子点，pass
        r, c = pos
        if r == -1 and c == -1:
            # pass
            self.step += 1  # 记录步数
            self.record.append([r, c])  # 记录棋谱
            self.current_piece = -self.current_piece  # 不落子但改变棋子颜色
            self.caculateAllPoint()  # 预先判断下一步的所有可能走法
            return True

        if pos in self.validpointlist:
            # 当前位置是合法位置，可以落子
            self.board[r][c] = self.current_piece  # 在当前位置落子
            self.step += 1  # 记录步数
            self.record.append([r, c])  # 记录棋谱
            p = self.validpointlist.index(pos)  # 取得当前位置在合法落子点列表中的序号
            for r, c in self.reverslist[p]:  # 取得翻转棋子的位置，开始翻转棋子
                self.board[r][c] = self.current_piece

            self.getScore()  # 落子后重新计算分数
            self.current_piece = -self.current_piece  # 落子后改变棋子颜色
            self.caculateAllPoint()  # 预先判断下一步的所有可能走法
            return True
        else:
            return False

    def judgeWinLose(self):
        # 当整个棋盘都放满棋子，或者双方都没有合理走法（没有棋子可翻转），或者一方棋子全部被翻转（棋子数为0）
        # 则一局告终，棋子多的一方获胜
        # 返回胜负信息；返回False则说明没有胜负，继续下棋
        if self.score[0] + self.score[1] == 64 or (self.enabalemove[0] == False and self.enabalemove[1] == False) or \
                (self.score[0] == 0 or self.score[1] == 0):
            if self.score[0] > self.score[1]:
                msg = "本局黑方胜利"
                self.roundscore[0] += 1
                self.round += 1
            elif self.score[0] < self.score[1]:
                msg = "本局白方胜利"
                self.roundscore[1] += 1
                self.round += 1
            elif self.score[0] == self.score[1]:
                msg = "本局平局"
                self.roundscore[1] += 1
                self.roundscore[0] += 1
                self.round += 2
            return msg
        else:
            return False

    def judgeGameOver(self):
        # 五局三胜
        if self.roundscore[0] >= 3 or self.roundscore[1] >= 3:
            if self.roundscore[0] >= 3:
                msg = "本次比赛黑方胜利"
            elif self.roundscore[1] >= 3:
                msg = "本次比赛白方胜利"
            return msg
        else:
            return False

    def undo(self):
        # stp为悔棋几步
        stp = 1
        if self.people2machine:
            stp = 2
        if len(self.record) - stp >= 0:
            for i in range(stp):
                if len(self.record) <= 0:
                    pygame.display.quit()
                    print("undo error!!")
                    sys.exit()
                self.record.pop()  # 删除最近的一步棋
            rec = self.record[:]  # 复制下棋记录
            self.resetBoard()  # 棋盘复原
            for r, c in rec:
                self.addPiece([r, c])  # 从头开始复盘
            return True
        else:
            return False

    def giveup(self):
        # 认输，为对方加分
        if self.current_piece == -1:
            self.roundscore[1] += 1
        else:
            self.roundscore[0] += 1
        self.resetBoard()

    def currentEnableMove(self):
        i = 0
        if self.current_piece == 1:
            i = 1
        return self.enabalemove[i]

    def currentPlayer(self):
        i = 0
        if self.current_piece == 1:
            i = 1
        return self.player[i]


class Interface:
    # 棋盘显示及操作层
    def __init__(self):
        self.BoardSize = 550
        self.BoardTopLeft = 24
        self.BoardRightBottom = 572
        self.GridSize = 68.5  # 棋盘格子的尺寸
        self.buttontop = 180
        self.buttonbottom = 204
        self.buttonleft = 628
        self.buttonright = 876
        self.bsize = 62  # 按钮尺寸
        self.debug = False
        self.surflist = []
        self.msgsurf = pygame.image.load("msgbox.png")
        self.passsurf = pygame.image.load("pass.png")
        self.startsurf = pygame.image.load("startmenu.png")
        pygame.init()
        self.win = pygame.display.set_mode([900, 600])
        pygame.display.set_caption("黑白棋 ver0.1")

    def drawPassBox(self):
        # 显示pass提示画面
        # 先保存当前屏幕
        bk_surf = pygame.Surface.copy(self.win)
        self.win.blit(self.passsurf, [160, 160])
        pygame.display.flip()
        time.sleep(1)
        self.win.blit(bk_surf, [0, 0])
        pygame.display.flip()

    def drawMsgBox(self, msg):
        # 显示确认对话框
        # 先保存当前屏幕
        bk_surf = pygame.Surface.copy(self.win)
        # 绘制对话框
        self.win.blit(self.msgsurf, [92, 162])
        font = pygame.font.Font("FZLBFW.ttf", 32)  # 汉字大小
        str1_surf = font.render(msg, 1, (0, 0, 0))
        self.win.blit(str1_surf, [170, 250])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cursor_x = event.pos[0]  # 取得x坐标
                    cursor_y = event.pos[1]
                    row, col = self.cursor2Button(cursor_x, cursor_y)
                    if row == 4 and col == 3:
                        # 还原屏幕显示
                        self.win.blit(bk_surf, [0, 0])
                        pygame.display.flip()
                        return True
                    elif row == 4 and col == 4:
                        self.win.blit(bk_surf, [0, 0])
                        pygame.display.flip()
                        return False

    def drawStartMenu(self):
        self.win.blit(self.startsurf, [0, 0])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cursor_x = event.pos[0]  # 取得x坐标
                    cursor_y = event.pos[1]
                    row, col = self.cursor2Button(cursor_x, cursor_y)
                    if col >= 2 and col <= 5:
                        if row == 5:
                            return True
                        elif row == 3:
                            return False

    def selectPlayer(self, reversi):
        choice = self.drawStartMenu()
        if choice:
            # 人机对战
            self.surflist.append(pygame.image.load("qipan9x6_b_m.png"))
            self.surflist.append(pygame.image.load("qipan9x6_w_m.png"))
        else:
            # 人人对战
            reversi.player[1] = 'people'
            self.surflist.append(pygame.image.load("qipan9x6_b.png"))
            self.surflist.append(pygame.image.load("qipan9x6_w.png"))

        self.surflist.append(pygame.image.load("qizi_black.png"))
        self.surflist.append(pygame.image.load("qizi_white.png"))
        self.surflist.append(pygame.image.load("qizi_tishi3.png"))
        self.surflist.append(pygame.image.load("qizi_black_box.png"))
        self.surflist.append(pygame.image.load("qizi_white_box.png"))
        self.surflist.append(pygame.image.load("qizi_animate.png"))

    def pieceAnimate(self, pos, dir):
        # 棋子翻转动画
        # self.surflist[0]是背景棋盘，self.surflist[7]是棋子动画序列
        # pos[r,c]为棋盘中的位置
        # dir=1黑变白，dir=-1白变黑
        framerate = pygame.time.Clock()
        r, c = pos
        px = c * self.GridSize + self.BoardTopLeft
        py = r * self.GridSize + self.BoardTopLeft
        i = 0
        if dir == 1:
            i = 0
        elif dir == -1:
            i = 9

        for j in range(10):
            framerate.tick(30)
            imgrect = pygame.Rect(i * 69, 0, 69, 70)
            piece_img = self.surflist[7].subsurface(imgrect)
            back_img = self.surflist[0].subsurface(px, py, 69, 70)
            self.win.blit(back_img, [px, py])
            self.win.blit(piece_img, [px, py])
            pygame.display.flip()
            i += dir

    def drawScreenAddPiece(self, reversi, moveorpass, bpos):
        # 绘制棋盘并更新棋盘数据
        # reversi为棋盘数据，bpos为落子点的坐标[row,col]
        # moveorpass(True or False):走棋或者pass的状态量

        # 更换背景左半边
        back_left = self.surflist[0].subsurface(0, 0, 600, 600)
        self.win.blit(back_left, [0, 0])

        # 开始显示整个棋盘上的黑白子
        for r in range(8):
            for c in range(8):
                px = c * self.GridSize + self.BoardTopLeft
                py = r * self.GridSize + self.BoardTopLeft
                if reversi.board[r][c] == -1:
                    # 黑棋
                    self.win.blit(self.surflist[2], [px, py])
                elif reversi.board[r][c] == 1:
                    # 白棋
                    self.win.blit(self.surflist[3], [px, py])
        pygame.display.flip()

        r, c = bpos
        if moveorpass:
            # 是实际落子或者pass
            if r != -1 and c != -1:
                # 有落子操作，开始显示当前落子棋
                px = c * self.GridSize + self.BoardTopLeft
                py = r * self.GridSize + self.BoardTopLeft
                if reversi.current_piece == -1:
                    # 黑棋带框
                    self.win.blit(self.surflist[5], [px, py])
                elif reversi.current_piece == 1:
                    # 白棋带框
                    self.win.blit(self.surflist[6], [px, py])
                pygame.display.flip()

                # 开始翻转棋子

                if reversi.current_piece == -1:
                    dir = -1
                else:
                    dir = 1
                for p in reversi.actual_revlst:
                    self.pieceAnimate(p, dir)
            else:
                self.drawPassBox()

            # 真正改变棋盘数据结构
            reversi.addPiece(bpos)

        # 显示新的提示棋
        for r in range(8):
            for c in range(8):
                if reversi.board[r][c] >= 100:
                    px = c * self.GridSize + self.BoardTopLeft
                    py = r * self.GridSize + self.BoardTopLeft
                    # 提示棋
                    self.win.blit(self.surflist[4], [px, py])
                    if self.debug:
                        # 显示各个合法位置的翻转棋子的数量
                        str2 = str(reversi.board[r][c] - 100)
                        txt2_surf = font1.render(str2, 1, (0, 0, 0))
                        self.win.blit(txt2_surf, [px + 25, py + 25])
        pygame.display.flip()

        # 根据当前棋子更换背景右半边
        if reversi.current_piece == -1:
            back_right = self.surflist[0].subsurface(600, 0, 300, 600)
        else:
            back_right = self.surflist[1].subsurface(600, 0, 300, 600)
        self.win.blit(back_right, [600, 0])

        hz = ['零', '壹', '贰', '叁', '肆', '伍']
        font1 = pygame.font.Font("FZLBFW.ttf", 20)  # 数字大小
        font2 = pygame.font.Font("FZLBFW.ttf", 32)  # 汉字大小

        # 显示button坐标
        str1 = str(bpos[0]) + " , " + str(bpos[1])
        str1_surf = font1.render(str1, 1, (0, 0, 0))
        self.win.blit(str1_surf, [640, 237])

        # 显示当前局的比分
        scorestr1 = str(reversi.score[0]) + " : " + str(reversi.score[1])
        score_surf1 = font1.render(scorestr1, 1, (94, 39, 7))
        # 显示总比分
        scorestr2 = str(hz[reversi.roundscore[0]]) + " : " + str(hz[reversi.roundscore[1]])
        score_surf2 = font2.render(scorestr2, 1, (150, 0, 0))
        # 显示步数
        str2 = str(reversi.step)
        str2_surf = font1.render(str2, 1, (0, 0, 0))
        self.win.blit(str2_surf, [830, 237])

        self.win.blit(score_surf1, [730, 85])
        self.win.blit(score_surf2, [710, 32])
        pygame.display.flip()

    def showLastPiece(self, reversi):
        # 将下棋记录里的最后一步棋，显示为当前落子
        if len(reversi.record) > 0:
            # 取最后一步棋
            r, c = reversi.record[len(reversi.record) - 1]
            px = c * self.GridSize + self.BoardTopLeft
            py = r * self.GridSize + self.BoardTopLeft
            if reversi.board[r][c] == -1:
                # 黑棋带框
                self.win.blit(self.surflist[5], [px, py])
            elif reversi.board[r][c] == 1:
                # 白棋带框
                self.win.blit(self.surflist[6], [px, py])
            pygame.display.flip()

    def cursor2Button(self, x, y):
        # 屏幕光标位置转换为按钮
        # [0,0]~[7,7]为棋盘相应格子
        # [10,0]~[10,3]为四个控制按钮
        # [-100,-100]为不合法的点击
        row = -100
        col = -100
        if x >= self.BoardTopLeft and x <= self.BoardRightBottom and y >= self.BoardTopLeft and y <= self.BoardRightBottom:
            row = int((y - self.BoardTopLeft) / self.GridSize)
            col = int((x - self.BoardTopLeft) / self.GridSize)
        elif x >= self.buttonleft and x <= self.buttonright and y >= self.buttontop and y <= self.buttonbottom:
            row = 10
            col = int((x - self.buttonleft) / self.bsize)
        return row, col

    def getPlayerInput(self, reversi):
        # 得到正确的输入
        # 返回值为(-1,-1):当前没有合理走法
        # 返回值为(10，0)~(10，3):四个按钮及窗口关闭按钮
        # 返回值为(0，0)~(7，7):合理的走法
        if reversi.currentEnableMove():
            # 当前棋子有合理走法，进行下一步判断
            if reversi.currentPlayer() == 'people':
                while True:
                    # 等待有效的落子
                    for event in pygame.event.get():
                        # 开始等待玩家落子或选择按钮
                        if event.type == pygame.QUIT:
                            # 由后面的程序统一处理退出
                            return [10, 0]
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            row, col = self.cursor2Button(event.pos[0], event.pos[1])
                            if row == -100 and col == -100:
                                # 无效的点击，进入下一次循环等待
                                continue
                            elif row == 10:
                                # 返回按钮值
                                return [row, col]
                            else:
                                # 棋盘格内的点击
                                if [row, col] in reversi.validpointlist:
                                    # 是有效的点击，返回
                                    return [row, col]
            else:
                return reversi.computerMove()
        else:
            return [-1, -1]

    def inputRespond(self, reversi, pos):
        # 根据鼠标输入，执行相应操作，做出响应
        row, col = pos
        if row == 10 and col == 0:
            # 离开，即退出游戏
            # 需增加确认环节，防止误操作
            if self.drawMsgBox("娱乐结束退出游戏"):
                return False

        elif row == 10 and col == 1:
            # 悔棋
            if reversi.undo():
                self.drawScreenAddPiece(reversi, False, [-1, -1])
                self.showLastPiece(reversi)

        elif row == 10 and col == 2:
            # 认输
            # 需增加确认环节，防止误操作
            if self.drawMsgBox("本局认输再来一盘"):
                reversi.giveup()
                self.drawScreenAddPiece(reversi, False, [-1, -1])

        elif row == 10 and col == 3:
            # 当前局重玩，不影响总比分
            # 需增加确认环节，防止误操作
            if self.drawMsgBox("本局不算重来一盘"):
                reversi.resetBoard()
                self.drawScreenAddPiece(reversi, False, [-1, -1])

        else:
            # 合理输入或者pass
            reversi.getActualRevlst([row, col])
            self.drawScreenAddPiece(reversi, True, [row, col])
        return True


# main

myreversi = Reversi(-1)
myinterface = Interface()

myinterface.selectPlayer(myreversi)
myinterface.drawScreenAddPiece(myreversi, False, [-1, -1])

roundover = False
while not roundover:
    roundscore = myreversi.judgeWinLose()
    if roundscore == False:
        # 没有胜负，继续比赛
        roundover = False
        pos = myinterface.getPlayerInput(myreversi)
        res = myinterface.inputRespond(myreversi, pos)
        if res == False:
            # 玩家选择退出程序
            roundover = True
            break
        time.sleep(0.5)
        continue
    else:
        # 有胜负，显示对话框，一局结束
        myinterface.drawMsgBox(roundscore)
        myreversi.resetBoard()
        myinterface.drawScreenAddPiece(myreversi, False, [-1, -1])
        roundover = True

pygame.display.quit()
print("Player select quit game")
sys.exit()
