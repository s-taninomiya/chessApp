from pieces import *
from copy import copy
from OpenGL.GL import *
from OpenGL.GLUT import *
from utils import *
import sys

uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }}
WSIZE = 720     # 画面サイズ
opponent = {WHITE: BLACK,BLACK: WHITE}

class Game:
    #ive decided since the number of pieces is capped but the type of pieces is not (pawn transformations), I've already coded much of the modularity to support just using a dictionary of pieces
    def __init__(self):
        self.playersturn = WHITE
        self.message = "this is where prompts will go"
        self.gameboard = {}
        self.placePieces()
        print("chess program. enter moves in algebraic notation separated by space")
        self.glmain()
        
        self.main()
        

        
    def placePieces(self):

        for i in range(0,8):
            self.gameboard[(i,1)] = Pawn(WHITE,uniDict[WHITE][Pawn],1)
            self.gameboard[(i,6)] = Pawn(BLACK,uniDict[BLACK][Pawn],-1)
            
        placers = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
        
        for i in range(0,8):
            self.gameboard[(i,0)] = placers[i](WHITE,uniDict[WHITE][placers[i]])
            self.gameboard[(i,7)] = placers[i](BLACK,uniDict[BLACK][placers[i]])
        placers.reverse()

        
    def main(self):
        #while True:
            self.printBoard()
            print(self.message)
            self.message = ""
            startpos,endpos = self.parseInput()
            try:
                target = self.gameboard[startpos]
            except:
                self.message = "could not find piece; index probably out of range"
                target = None
                
            if target:
                print("found "+str(target))
                if target.Color != self.playersturn:
                    self.message = "you aren't allowed to move that piece this turn"
                if self.isValidMove(startpos,endpos,target.Color,self.gameboard):
                    self.message = "that is a valid move"
                    self.renewGameboard(startpos,endpos,self.gameboard)
                    if self.isCheck(target.Color,self.gameboard):
                        self.message = f"{target.Color} player is in check"
                    if self.cannotMove(target.Color, self.gameboard):
                        if self.isCheck(target.Color, self.gameboard):
                            self.message = f"Checkmate! {opponent[target.Color]} player won!"
                            sys.exit()
                        else:
                            self.message = "Stalemate! It's draw."
                            sys.exit()
                    if self.playersturn == BLACK:
                        self.playersturn = WHITE
                    else : self.playersturn = BLACK
                else : 
                    self.message = "invalid move" + str(target.availableMoves(startpos[0],startpos[1],self.gameboard))
                    print(target.availableMoves(startpos[0],startpos[1],self.gameboard))
            else : self.message = "there is no piece in that space"

    def isValidMode(self,piece,startpos,endpos,gameboard):
        if endpos in piece.availableMoves(startpos[0],startpos[1],gameboard, Color = piece.Color):
            #盤面の複製
            gameboardTmp = copy(gameboard)
            #複製した盤面の更新
            self.renewGameboard(startpos,endpos,gameboardTmp)
            #チェック判定
            if self.isCheck(piece.Color,gameboardTmp):
                return False
            else:
                return True
        else:
            return False
        
    def isCheck(self, color, gameboard):
        #ascertain where the kings are, check all pieces of opposing color against those kings, then if either get hit, check if its checkmate
        king = King
        kingDict = {}
        pieceDict = {BLACK : [], WHITE : []}
        for position,piece in gameboard.items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece,position))
        #white
        if self.canSeeking(kingDict[color],pieceDict[opponent[color]],gameboard):
            return True
        
    def canSeeKing(self,kingpos,piecelist,gameboard):
        #checks if any pieces in piece list (which is an array of (piece,position) tuples) can see the king in kingpos
        for piece,position in piecelist:
            if piece.isValid(position,kingpos,piece.Color,gameboard):
                return True

    def cannotMove(self, color, gameboard):
        '''color側が駒を動かせないときTrueを返す'''
        for position, piece in gameboard.items():
            # 盤面上の駒の位置と駒について
            if color == piece.Color:
                # 駒色がcolorのとき
                for dest in piece.availableMoves(*position, gameboard, Color=color):
                    # 駒の移動先について
                    # 移動後にチェック回避できるならFalse
                    gameboardTmp = copy(gameboard)
                    self.renewGameboard(position,dest,gameboardTmp)
                    if not self.isCheck(color, gameboardTmp):
                        return False
        # colorのどの駒をどのように移動させてもチェック回避できなかったとき
        return True

    def renewGameboard(self, startpos, endpos, gameboard):
            '''盤面を更新する'''
            gameboard[endpos] = gameboard[startpos]
            del gameboard[startpos]

    def parseInput(self):
        try:
            a,b = input().split()
            a = ((ord(a[0])-97), int(a[1])-1)
            b = (ord(b[0])-97, int(b[1])-1)
            print(a,b)
            return (a,b)
        except:
            print("error decoding input. please try again")
            return((-1,-1),(-1,-1))
        
    def printBoard(self):
        print("  1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
        for i in range(0,8):
            print("-"*32)
            print(chr(i+97),end="|")
            for j in range(0,8):
                item = self.gameboard.get((i,j)," ")
                print(str(item)+' |', end = " ")
            print()
        print("-"*32)

    def draw(self):
        '''描画コールバック'''
        glClearColor(0.6, 0.4, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glColor(1, 0, 0)
        #square(0, 0)
        draw_squares()
        draw_file()
        draw_rank()
        glutSwapBuffers()   # 強制描画
        
    def glmain(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)    # 表示設定
        glutInitWindowSize(WSIZE, WSIZE)                # 画面サイズ
        glutInitWindowPosition(0, 0)                    # 画面の表示位置
        glutCreateWindow(b'Chess')                      # ウィンドウの名前
        glutDisplayFunc(self.draw)                      # 描画
        glOrtho(-1.0, 8.0, -1.0, 8.0, -4, 4)
        glutMainLoop()

Game()
