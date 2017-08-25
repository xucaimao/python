#python游戏编程快速上手
#Reversi游戏

import pygame, random, sys, time

#定义棋盘相对于窗口的偏移量、棋盘大小
global DX,DY


def drawBoard(win,bk_surf,pos,b_surf,w_surf,board):
    #绘制棋盘,win为棋盘所在窗口，pos为左上角坐标
    #bk_surf为背景图的Surface,b_surf,w_surf为黑棋和白棋的Surface
    win.blit(bk_surf,pos)
    offset=4
    for r in range(8):
        for c in range(8):
            if board[r][c] == -1:
                win.blit(b_surf, [c * 75 + pos[0] + offset, r * 75 + pos[1] + offset])
            elif board[r][c] == 1:
                win.blit(w_surf, [c * 75 + pos[0] + offset, r * 75 + pos[1] + offset])


def drawText(win,str1,str2,str3):
    txtbackimg = pygame.image.load("reverse_board2.png")
    font1=pygame.font.Font(None,20)
    txt1_surf=font1.render(str1,1,(0,0,0))
    txt2_surf = font1.render(str2, 1, (255, 0, 0))
    txt3_surf=font1.render(str3, 1, (0, 0, 255))
    win.blit(txtbackimg, [601, 0])
    win.blit(txt1_surf,[605,0])
    win.blit(txt2_surf, [605, 50])
    win.blit(txt3_surf, [605, 100])


def resetBoard(board):
    #游戏数据清零,每个玩家有两个棋子在棋盘的中央
    #用于开始新游戏
    for r in range(8):
        for c in range(8):
            board[r][c]=0
    board[3][3]=-1
    board[3][4]=1
    board[4][3]=1
    board[4][4]=-1

def getNewBoard():
    #创建新的数据表，用于程序初始化
    board=[]
    for i in range(8):
        board.append([0]*8)
    return board

def isOnBoard(x,y):
    if x >= 0 and x <= 7 and y >= 0 and y <= 7:
        return True
    else:
        return False



def judge2(board,player,row,col):
    #书上的方法，比较啰嗦
    #在棋盘上根据在行列row,col上的落子player，进行计算
    #返回要反转的棋子的列表
    tilesToFlip=[]
    dir = [[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]]
    # 八个方向遍历
    for i in range(8):
        r,c=row,col
        r += dir[i][1]
        c += dir[i][0]
        if isOnBoard(r,c) and board[r][c]== -player:
            #找到对方的棋子,接着看下一个棋子
            r += dir[i][1]
            c += dir[i][0]
            if not isOnBoard(r,c):
                #下一棋子不在棋盘上，则开始遍历下一个方向(开始下一个for循环)
                continue
            while board[r][c] == -player:
                #如果下一棋子是对方棋子，则继续找下去
                r += dir[i][1]
                c += dir[i][0]
                if not isOnBoard(r,c):
                    #不在棋盘上，则退出while循环
                    break
            if not isOnBoard(r,c):
                #下一棋子不在棋盘上，则开始遍历下一个方向(开始下一个for循环)
                continue
            if board[r][c] == player:
                #找到下一个本方棋子,则开始记录要反转的棋子坐标
                while True:
                    r -= dir[i][1]
                    c -= dir[i][0]
                    if r==row and c==col:
                        break
                    tilesToFlip.append([r,c])

    return tilesToFlip


def judge(board,player,row,col):
    #在棋盘上根据在行列row,col上的落子player，进行计算
    dir=[ [1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1] ]

    reverlist = []          #八个方向的总列表
    #八个方向遍历
    for i in range(8):
        revli=[]            #一个方向的小列表
        r=row
        c=col
        while True:
            r+=dir[i][1]
            c+=dir[i][0]
            if isOnBoard(r,c):
                if board[r][c]== -player:
                    #只有遇到对方棋子，就在小列表中记录其坐标
                    revli.append([r,c])
                elif board[r][c]==player:
                    #遇到同色棋子，把小列表并入大列表，
                    # 退出while循环,进入下一个方向的判断
                    for rr,cc in revli:
                        reverlist.append([rr,cc])
                    break
                elif board[r][c]==0:
                    #遇到空白则退出whie循环，进入下一个方向的判断
                    break
            else:
                #超出棋盘的范围
                break
    if len(reverlist)==0:
        return False
    return reverlist

def getScore(board):
    bscore=0
    wscore=0
    for r in range(8):
        for c in range(8):
            if board[r][c]==-1:
                bscore+=1
            elif board[r][c]==1:
                wscore+=1
    return bscore,wscore


#main

pygame.init()
screen=pygame.display.set_mode([800,600])
screen.fill([255,255,255])
bd_img=pygame.image.load("reverse_board.png")

p_b_img=pygame.image.load("pieces_black.png")
p_w_img=pygame.image.load("pieces_white.png")

DX=0
DY=0
#黑棋先手
player=-1
pplayer=-1
#生成棋盘数据
myboard=getNewBoard()
resetBoard(myboard)
drawBoard(screen,bd_img,[DX,DY],p_b_img,p_w_img,myboard)
pygame.display.flip()

while True:
    #screen.fill([255, 255, 255])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #屏幕光标与数据结构内的行列的转换
            p_col=int( (event.pos[0]-DX)/75 )
            p_row=int( (event.pos[1]-DY)/75 )
            #鼠标状态信息显示
            str1 = str(event.pos[0]) + " , " + str(event.pos[1])
            str2=str(p_row)+" , "+str(p_col)

            if isOnBoard(p_col,p_row) and myboard[p_row][p_col]==0:
                #落子有效
                myboard[p_row][p_col]=player
                pplayer=player
                player*=-1
            #显示落子的变化
            drawBoard(screen, bd_img, [DX, DY], p_b_img, p_w_img, myboard)
            pygame.display.flip()
            #根据规则进行计算,延时2秒刷新屏幕
            listflip=judge(myboard,pplayer,p_row,p_col)
            str3=""
            for r,c in listflip:
                str3+=" : "+str(r)+" , "+str(c)
                myboard[r][c]=pplayer
            drawText(screen, str1, str2,str3)
            time.sleep(1)
            drawBoard(screen, bd_img, [DX, DY], p_b_img, p_w_img, myboard)
            pygame.display.flip()

