#黑白棋
#根据书上程序，结合苹果手机里的一款黑白棋游戏，进行修改
#采用面向对象的方法编程
#待改进处：
#一个底纹，根据选择进行合成，显示
#实现了动态显示棋子翻转过程。对整个显示的逻辑进行了重大的调整

import pygame,sys,time

class Reversi:
    # 棋盘(二维列表)-1黑棋，0空格，1白棋，>100则表示该位置是一种合理的落子点，
    # 其值减去100所得结果，表示在改点落子后，可以翻转的对方棋子的数量
    def __init__(self,stpiece):
        self.start_piece=stpiece        # 初始棋子，即谁先走
        self.board=[]                   # 棋盘(二维列表)。-1黑棋，0空格，1白棋，>=100则表示改位置是一种合理的走棋点，
        self.current_piece=stpiece      # 当前下棋的棋子颜色
        self.enabalemove=False          # 当前棋子有没有合法的落子点，如果没有就需要通过成绩比较判断输赢
        self.pointlist=[]               # 如果有合法落子点，则记录所有的位置坐标的列表(一维列表，每个元素是一个棋子坐标)
        self.reverslist=[]              # 每个合法落子所对应的可翻转的对方棋子的坐标列表(二维列表，每个元素是一个列表)
        self.endrevlst=[]               # 最终选择的落子所对应的可翻转的对方棋子的坐标列表(一维列表，每个元素是一个棋子坐标)
        self.round=0                    # 第几局比赛
        self.roundscore=[0,0]           # 大比分
        self.score = [0,0]              # 当前局比分(黑比白)
        self.step=0                     # 当前局步数
        self.record=[]                  # 棋谱记录.undo可以通过棋谱从第一步开始计算的形式，以计算时间换取存储空间(一维列表)
        self.resetBoard()

    def clearlist(self,l):
        #清空列表
        while l:
            l.pop()
        return l

    def resetBoard(self):
        # 游戏数据清零,每个玩家有两个棋子在棋盘的中央
        # 用于开始新游戏
        # 需要增加考虑白棋先行的情况
        self.clearlist(self.board)
        for i in range(8):
            self.board.append([0] * 8)
        self.board[3][3] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = -1

        self.current_piece = self.start_piece
        self.score =2,2
        self.step = 0
        self.clearlist(self.pointlist)
        self.clearlist(self.reverslist)
        self.clearlist(self.endrevlst)
        self.clearlist(self.record)

        self.judge_allpoint()


    def isOnBoard(self,x, y):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            return True
        else:
            return False

    def judge_point(self, pos):
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

    def judge_allpoint(self):
        # 判断当前棋子current_piece的所有可能的落子点
        # 落子点坐标存在pointlist列表中
        # 每个落子点对应的可以翻转的对方棋子的坐标存在reverslist列表中
        #如果没有合法落子点(pointlist列表为空)，则返回False。否则返回True
        self.clearlist(self.pointlist)
        self.clearlist(self.reverslist)
        self.clearlist(self.endrevlst)

        # 清理辅助棋子数据
        for r in range(8):
            for c in range(8):
                if self.board[r][c] >= 100:
                    self.board[r][c] = 0
        # 开始遍历所有空白棋格
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 0:
                    revlst = self.judge_point([r, c])
                    if revlst == False:
                        # 该位置不能落子，开始下一个for循环
                        continue
                    else:
                        # 在复制的数据里记录位置数据
                        self.board[r][c] = 100 + len(revlst)
                        self.pointlist.append([r,c])
                        self.reverslist.append(revlst)
        #设置当前棋子有无合法落子点的标志
        if len(self.pointlist) == 0:
            self.enabalemove = False    #此语句及变量应该可以取消，后期调试看再优化
            return False
        else:
            self.enabalemove = True     #此语句及变量应该可以取消，后期调试看再优化
            return True

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
                maxpiece = self.board[r][c]

        return maxrow, maxcol

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
        self.score=bscore,wscore

    def getround(self):
        return self.round

    def setround(self,rd):
        self.round=rd

    def judgeplayermove(self,pos):
        #判断玩家在在当前位置pos[row,col]处落子是否合法
        #如果合法则返回翻转棋子的列表，用于动画显示
        #否则返回False
        if pos in self.pointlist:
            #当前位置是合法位置，可以落子
            p=self.pointlist.index(pos)                 #取得当前位置在合法落子点列表中的序号
            for r,c in self.reverslist[p]:              #取得翻转棋子的位置，开始翻转棋子
                self.endrevlst.append([r,c])
            return True
        else:
            return False


    def addpiece(self,pos):
        #在当前位置pos[row,col]处落子
        if pos in self.pointlist:
            #当前位置是合法位置，可以落子
            r,c=pos
            self.board[r][c] = self.current_piece       #在当前位置落子
            #此处增加显示落子
            self.step+=1                                #记录步数
            self.record.append([r,c])                   #记录棋谱
            p=self.pointlist.index(pos)                 #取得当前位置在合法落子点列表中的序号
            for r,c in self.reverslist[p]:              #取得翻转棋子的位置，开始翻转棋子
                self.board[r][c]=self.current_piece

            self.getScore()                             #落子后重新计算分数
            self.current_piece=-self.current_piece      #落子后改变棋子颜色
            self.judge_allpoint()                       #预先判断下一步的所有可能走法
            return True
        else:
            return False


    def undo(self,stp):
        #stp为悔棋几步
        for i in range(stp):
            if len(self.record)<=0:
                pygame.display.quit()
                print("undo error!!")
                sys.exit()
            self.record.pop()                           #删除最近的一步棋
        rec=self.record[:]                              #复制下棋记录
        self.resetBoard()                               #棋盘复原
        for r,c in rec:
            self.addpiece([r,c])                        #从零开始复盘

    def giveup(self):
        #认输，为对方加分
        if self.current_piece==-1:
            self.roundscore[1] += 1
        else:
            self.roundscore[0] += 1
        self.resetBoard()


#function of main

#这些全局数据都是屏幕显示相关的，最好改成一个列表。将此列表作为参数，传入显示函数中
global BoardSize,BoardTopLeft,BoardRightBottom
global GridSize  #棋盘格子的尺寸
global buttontop,buttonbottom
global buttonleft,buttonright
global bsize     #按钮尺寸
BoardSize=550
BoardTopLeft=24
BoardRightBottom=572
GridSize=68.5  #棋盘格子的尺寸
buttontop=180
buttonbottom=204
buttonleft=628
buttonright=876
bsize=62     #按钮尺寸

global debug
debug=False         #为True则显示各个合法落子点对应的翻转对方棋子的数量

def drawmsgbox(win,surflist,msg):
    win.blit(surflist,[92,162])
    font = pygame.font.Font("FZLBFW.ttf", 32)  # 汉字大小
    str1_surf = font.render(msg, 1, (0, 0, 0))
    win.blit(str1_surf, [170,250])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor_x = event.pos[0]  # 取得x坐标
                cursor_y = event.pos[1]
                row, col = cursor2button(cursor_x, cursor_y)
                if row == 4 and col == 3:
                    return True
                elif row == 4 and col == 4:
                    return False

def drawstartmenu(win,surflist):
    win.blit(surflist,[0,0])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor_x = event.pos[0]  # 取得x坐标
                cursor_y = event.pos[1]
                row, col = cursor2button(cursor_x, cursor_y)
                if col>=2 and col <=5:
                    if row == 5:
                        return True
                    elif row == 3:
                        return False


def piece_animate(win,background,animateimg,pos,dir):
    #棋子翻转动画
    #background是背景棋盘，animateimg是棋子动画序列
    #pos[r,c]为棋盘中的位置
    #dir=1黑变白，dir=-1白变黑
    framerate = pygame.time.Clock()
    r,c=pos
    px=c * GridSize + BoardTopLeft
    py=r * GridSize + BoardTopLeft
    i=0
    if dir==1:
        i=0
    elif dir==-1:
        i = 9

    for j in range(10):
        framerate.tick(20)
        #ticks = pygame.time.get_ticks()

        imgrect = pygame.Rect(i * 69, 0, 69, 70)
        piece_img = animateimg.subsurface(imgrect)
        back_img = background.subsurface(px, py, 69, 70)

        win.blit(back_img, [px, py])
        win.blit(piece_img, [px, py])
        pygame.display.flip()
        i += dir

def drawscreen_addpiece(win,reversi,surflist,validpress,bpos):
    # 绘制棋盘,win为棋盘所在窗口，bpos为button的坐标[row,col]，此处只是为了测试程序，此参数可以删除
    # surflist为背景图黑棋行，背景图白棋行，黑棋，白棋和提示棋的Surface组成的列表
    #本程序用了一些屏幕坐标，后期可以改成列表将这些数据传入

    #更换背景左半边
    back_left=surflist[0].subsurface(0,0,600,600)
    win.blit(back_left, [0, 0])

    #开始显示整个棋盘上的黑白子
    for r in range(8):
        for c in range(8):
            px = c * GridSize + BoardTopLeft
            py = r * GridSize + BoardTopLeft
            if reversi.board[r][c] == -1:
                #黑棋
                win.blit(surflist[2], [px, py])
            elif reversi.board[r][c] == 1:
                #白棋
                win.blit(surflist[3], [px, py])
    pygame.display.flip()

    r,c=bpos
    if validpress:
        #有落子操作，开始显示当前落子棋
        px=c * GridSize + BoardTopLeft
        py=r * GridSize + BoardTopLeft
        if reversi.current_piece == -1:
            # 黑棋带框
            win.blit(surflist[5], [px, py])
        elif reversi.current_piece == 1:
            # 白棋带框
            win.blit(surflist[6], [px, py])
        pygame.display.flip()

        #开始翻转棋子

        if reversi.current_piece==-1:
            dir=-1
        else:
            dir=1
        for p in reversi.endrevlst:
            piece_animate(win,surflist[0],surflist[7],p,dir)


        #改变棋盘数据结构
        reversi.addpiece(bpos)

    #显示提示棋
    for r in range(8):
        for c in range(8):
            if reversi.board[r][c] >= 100:
                # 提示棋
                win.blit(surflist[4], [c * GridSize + BoardTopLeft, r * GridSize + BoardTopLeft])
                if debug:
                    # 显示各个合法位置的翻转棋子的数量
                    str2 = str(reversi.board[r][c] - 100)
                    txt2_surf = font1.render(str2, 1, (0, 0, 0))
                    win.blit(txt2_surf, [c * GridSize + BoardTopLeft + 25, r * GridSize + BoardTopLeft + 25])
    pygame.display.flip()

    # 根据当前棋子更换背景右半边
    if reversi.current_piece == -1:
        back_right = surflist[0].subsurface(600, 0, 300, 600)
    else:
        back_right = surflist[1].subsurface(600, 0, 300, 600)
    win.blit(back_right, [600, 0])

    hz = ['零', '壹', '贰', '叁', '肆', '伍']

    font1 = pygame.font.Font("FZLBFW.ttf", 20)  # 数字大小
    font2 = pygame.font.Font("FZLBFW.ttf", 32)  # 汉字大小
    # 显示button坐标
    str1 = str(bpos[0]) + " , " + str(bpos[1])
    str1_surf = font1.render(str1, 1, (0, 0, 0))
    # 显示当前局的比分
    scorestr1 = str(reversi.score[0]) + " : " + str(reversi.score[1])
    score_surf1 = font1.render(scorestr1, 1, (94, 39, 7))
    # 显示总比分
    scorestr2 = str(hz[reversi.roundscore[0]]) + " : " + str(hz[reversi.roundscore[1]])
    score_surf2 = font2.render(scorestr2, 1, (150, 0, 0))
    # 显示步数
    str2 = str(reversi.step)
    str2_surf = font1.render(str2, 1, (0, 0, 0))

    win.blit(str1_surf, [640, 237])
    win.blit(str2_surf, [830, 237])
    win.blit(score_surf1, [730, 85])
    win.blit(score_surf2, [710, 32])
    pygame.display.flip()

def cursor2button(x,y):
    #屏幕光标位置转换为按钮
    #[0,0]~[7,7]为棋盘相应格子
    #[10,0]~[10,3]为四个控制按钮
    #[-1,-1]为不合法的点击
    row=-1
    col=-1
    if x>=BoardTopLeft and x<=BoardRightBottom and y>=BoardTopLeft and y<=BoardRightBottom:
        row = int((y - BoardTopLeft) / GridSize)
        col = int((x - BoardTopLeft) / GridSize)
    elif x>=buttonleft and x<=buttonright and y>=buttontop and y<=buttonbottom:
        row=10
        col=int((x-buttonleft)/bsize)
    return row,col


#main
#main

pygame.init()
screen = pygame.display.set_mode([900, 600])
pygame.display.set_caption("黑白棋 ver0.1")
# firstpiece为先手棋子的颜色。此处可以扩展选择先手棋子的颜色
firstpiece = -1

msgsurf = pygame.image.load("msgbox.png")
startsurf = pygame.image.load("startmenu.png")
# 初始化用于显示的各种图片
surflist = []

choice = drawstartmenu(screen, startsurf)
if choice:
    people2machine = True
    surflist.append(pygame.image.load("qipan9x6_b_m.png"))
    surflist.append(pygame.image.load("qipan9x6_w_m.png"))
else:
    people2machine = False
    surflist.append(pygame.image.load("qipan9x6_b.png"))
    surflist.append(pygame.image.load("qipan9x6_w.png"))

surflist.append(pygame.image.load("qizi_black.png"))
surflist.append(pygame.image.load("qizi_white.png"))
surflist.append(pygame.image.load("qizi_tishi.png"))
surflist.append(pygame.image.load("qizi_black_box.png"))
surflist.append(pygame.image.load("qizi_white_box.png"))
surflist.append(pygame.image.load("qizi_animate.png"))

# 初始化由于显示的各个坐标
poslist = []

# 生成棋盘的实例
myreversi = Reversi(firstpiece)
drawscreen_addpiece(screen, myreversi, surflist,False, [-1, -1])
while True:
    #首先判胜负
    if myreversi.enabalemove==False:
        if myreversi.score[0] > myreversi.score[1]:
            msg="本局黑方胜利"
            myreversi.roundscore[0]+=1
        elif myreversi.score[0] < myreversi.score[1]:
            msg="本局白方胜利"
            myreversi.roundscore[1] += 1
        else:
            myreversi.roundscore[1] += 1
            myreversi.roundscore[0] += 1
        if drawmsgbox(screen, msgsurf, msg):
            myreversi.resetBoard()
        drawscreen_addpiece(screen, myreversi, surflist,False, [-1, -1])

        continue

    for event in pygame.event.get():
        #开始等待玩家落子或选择按钮
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            cursor_x=event.pos[0]                 #取得x坐标
            cursor_y=event.pos[1]
            row,col=cursor2button(cursor_x,cursor_y)
            #刷新屏幕
            drawscreen_addpiece(screen,myreversi,surflist,False, [row,col])

            if row==-1 and col ==-1:
                # 非法点击，提示音，进入下一次for循环
                continue

            if row==10 and col==0:
                # 离开，即退出游戏
                # 需增加确认环节，防止误操作
                if drawmsgbox(screen,msgsurf,"娱乐结束退出游戏"):
                    pygame.display.quit()
                    print("Player select quit game")
                    sys.exit()
                drawscreen_addpiece(screen, myreversi, surflist,False, [-1, -1])
                continue

            elif row==10 and col==1:
                # 悔棋
                if len(myreversi.record)>0:
                    if people2machine:
                        myreversi.undo(2)
                    else:
                        myreversi.undo(1)
                    drawscreen_addpiece(screen, myreversi, surflist, False, [-1, -1])

                continue

            elif row==10 and col==2:
                # 认输
                # 需增加确认环节，防止误操作
                if drawmsgbox(screen, msgsurf, "本局认输再来一盘"):
                    myreversi.giveup()
                drawscreen_addpiece(screen, myreversi, surflist, False, [-1, -1])
                continue

            elif row==10 and col==3:
                # 当前局重玩，不影响总比分
                # 需增加确认环节，防止误操作
                if drawmsgbox(screen, msgsurf, "本局不算重来一盘"):
                    myreversi.resetBoard()
                drawscreen_addpiece(screen, myreversi, surflist, False, [-1, -1])
                continue
            else:
                # 棋盘上的点击
                #要增加是否为合法位置的判断
                revlst=myreversi.judgeplayermove([row,col])
                if revlst:
                    #是合法落子点，则执行以下步骤
                    #显示最新落子
                    #翻转落子
                    #变更棋盘数据，再变更数据显示，切换当前玩家
                    drawscreen_addpiece(screen, myreversi, surflist, True, [row, col])

                    if people2machine:
                        #电脑走棋
                        rr,cc=myreversi.computermove()
                        revlst = myreversi.judgeplayermove([rr, cc])

                        drawscreen_addpiece(screen, myreversi, surflist, True,[rr, cc])


