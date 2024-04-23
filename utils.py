from OpenGL.GL import *
from OpenGL.GLUT import *
TTFONTNAME = "メイリオ.ttc"

dark_squares_list = ([(i, j) for i in range(0, 8, 2) for j in range(0, 8, 2)] + [(i, j) for i in range(1, 8, 2) for j in range(1, 8, 2)])

def square(x, y):
    '''
    正方形を描画する
    
    Parameters
    ----------
    x, y : float
        中心の座標．
    '''
    glPushMatrix()                  # 変形が及ぶ範囲の開始
    glTranslate(x, y, 0)            # 以下の対象を平行移動
    glBegin(GL_QUADS)               # 四角形の描画を宣言
    glVertex(-1.0 / 2, -1.0 / 2)    # 頂点１の座標
    glVertex(1.0 / 2, -1.0 / 2)     # 頂点２
    glVertex(1.0 / 2, 1.0 / 2)      # 頂点３
    glVertex(-1.0 / 2, 1.0 / 2)     # 頂点４
    glEnd()                         # 描画終了
    glPopMatrix()
     
def draw_squares():
     '''マス目を描画する'''
     for i in range(8):
         for j in range(8):
             if (i, j) in dark_squares_list:
                 glColor(0.82, 0.55, 0.28)
                 square(i, j)
             else:
                 glColor(1.00, 0.81, 0.62)
                 square(i, j)
                 

def draw_str(x, y, string, font = "GLUT_BITMAP_HELVETICA_18", gap = 0.25):
    '''
    文字列を描画する

    Parameters
    ----------
    x, y : float
        描画する座標．
    string : str
        描画する文字列．
    font : , default GLUT_BITMAP_HELVETICA_18
        フォント．以下から指定．
        GLUT_BITMAP_8_BY_13
        GLUT_BITMAP_9_BY_15
        GLUT_BITMAP_TIMES_ROMAN_10
        GLUT_BITMAP_TIMES_ROMAN_24
        GLUT_BITMAP_HELVETICA_10
        GLUT_BITMAP_HELVETICA_12
        GLUT_BITMAP_HELVETICA_18
    gap : float, default 0.25
        文字間隔．
    '''
    for k in range(len(string)):
        glRasterPos2f(x + gap*k, y)                 # 描画位置指定
        glutBitmapCharacter(font, ord(string[k]))   # 文字列描画
        
def draw_file():
    '''ファイルの文字を描画する'''
    glColor(1.0, 1.0, 1.0)
    for x in range(8):
        draw_str(x, -0.75, chr(x + 97))
        
def draw_rank():
    '''ランクの文字を描画する'''
    glColor(1.0, 1.0, 1.0)
    for y in range(8):
        draw_str(-0.75, y, str(y + 1))