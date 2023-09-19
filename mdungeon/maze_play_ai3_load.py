import PIL.Image
import PIL.ImageTk
import tkinter.messagebox as msgbox
import random
import global_value as g
from tkinter import *
#import nerural_network_9 from *
from neural_network_mlp import *
import os

movetime = 1
maxturn = 100

wallmode = False


# グローバル変数の初期化
#px, py = (2, 2)  # プレイヤーの座標 --- (*1)
g.px = 2
g.py = 2

# player_image = "icon_player3.png" # プレイヤーの画像ファイル
player_image = "icons\icon_robot_red.png" # プレイヤーの画像ファイル
# player_image = "icons\icon_small_player2.png" # プレイヤーの画像ファイル
# player_image = "icons\icon_robot_red_25.png" # プレイヤーの画像ファイル

tile_size = 50 # 描画タイルのサイズ
iconfile_wall = "icons\icon_wall.png"
iconfile_steps = "icons\icon_steps.png"
# iconfile_waap = "icons\icon_waap2.png"
iconfile_sougen = "icons\icon_sougen.png"
iconfile_sougen2 = "icons\icon_sougen2.png"
iconfile_robot = "icons\icon_robot_red.png"
iconfile_renga = "icons\icon_renga.png"
iconfile_shiro = "icons\icon_shiro2.png"

# プレイヤーの画像を読み込む --- (*3)
def load_wall(cv):
    # global canvas, img_wall, img_steps, img_waap, img_sougen ,img_renga, img_shiro 
    # canvas = cv

    g.img_wall = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_wall))
    g.img_steps = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_steps))
    # g.img_waap = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_waap))
    g.img_sougen = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_sougen))
    g.img_renga = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_renga))
    g.img_shiro = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_shiro))

    if wallmode == True:
        g.img_wall = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_sougen2))

    # draw_wall(canvas)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__))) # カレントディレクトリを移動する

    global map_data
    # 迷路データを読み込む
    map_data = load_map_from_tsv("maze5.tsv")
    # NNを作る
    g.turn = 0
    create_nn()
    # init_env()#test
    nn.nn_load("nn")
    # ウィンドウを作成 --- (*2)
    create_window(map_data, [load_image, set_event])


def init_env():
    g.px = 2
    g.py = 2
    g.turn = 0


def calc_distance_goal():
    distance = (19-g.px)+(19-g.py)
    return distance

def create_nn():
    # ニューラルネットワークのインスタンス
    global nn
    nn = NeuralNetwork()

def run_nn():
    # 実行
    input_data = get_around_data()
    ret = nn.commit(input_data) 
    # print(ret)
    return ret

# ウィンドウとキャンバスを作成
def create_window(map_data, events = []):
    g.win = Tk()
    g.win.title("迷路") # --- (*6)
    rows = len(map_data)    # 迷路の行数
    cols = len(map_data[0]) # 迷路の列数
    g.cv = Canvas(g.win,
            width=(cols * tile_size), 
            height=(rows * tile_size))
    g.cv.pack()
    load_wall(g.cv)
    draw_map(g.cv, map_data)
    g.win.after(movetime, change_label_text,) 

    # 追加処理があればここで処理する --- (*7)
    for func in events: func(g.cv, map_data)

    g.win.mainloop()



def change_label_text():
    #100ms後にchange_label_textを実行
    g.turn = g.turn + 1
    g.win.title("迷路"+str(g.turn))
    print("[{2}] player={0},{1},".format(g.px, g.py, g.turn))

    if(g.turn > maxturn):
        init_env()

    ret = run_nn()
    div = round(ret/0.25)
    print("ret = " + str(ret) +" div="+str(div))

    # ran = random.randint(1, 4)
    ran = div

    if(ran == 1):
        move(1, 0)
    elif(ran == 2):
        move(0, 1)
    elif(ran == 3):
        move(-1, 0)
    elif(ran == 4):
        move(0, -1)

    get_around_data()

    g.win.after(movetime, change_label_text,) 


#----------------------------------

# CSV(タブ区切り)を読み込む
def load_map_from_tsv(filename):
    # ファイルを開く --- (*1)
    fp = open(filename, "rt", encoding="utf-8")
    tsv = fp.read()
    # TSVファイルを解析する
    rows = tsv.split("\n") # 改行で区切る --- (*2)
    result = []
    for line in rows:
        cols = line.split("\t") # タブで区切る --- (*3)
        if len(cols) <= 1: break
        cols = list(map(int, cols)) # ---(*4)
        result.append(cols)
    return result


# プレイヤーの画像を読み込む --- (*3)
def load_image(cv, map_data):
    global canvas, img_tk
    canvas = cv
    img = PIL.Image.open(player_image)
    img_tk = PIL.ImageTk.PhotoImage(img)
    draw_player(canvas)

# プレイヤーを描画 --- (*4)
def draw_player(cv):
    x = g.px * tile_size
    y = g.py * tile_size
    cv.create_image(x, y, image=img_tk, anchor=NW)

# マウスイベントを登録する --- (*5)
def set_event(cv, maze_data):
    cv.bind("<1>", canvas_click)

# キャンバスをクリックした時の処理 --- (*6)
def canvas_click(e):
    # global px, py
    # マウス座標を得る --- (*7)
    mx = e.x # マウスのX座標
    my = e.y # マウスのY座標
    # 移動前に前回の値を覚えておく
    px_tmp = g.px
    py_tmp = g.py
    # プレイヤーが上下左右のどちらに動くか判定 --- (*8)
    # プレイヤーの絶対座標を計算
    xx, yy = [px * tile_size + 25, g.py * tile_size + 25]
    ix = mx - xx
    iy = my - yy
    if abs(ix) > abs(iy): # 左右移動
        if ix > 0: px += 1
        else: px -= 1
    else: # 上下移動
        if iy > 0: g.py += 1
        else: g.py -= 1
    # 移動先がマップデータ外なら戻す --- (*9)
    if g.px < 0 or g.px >= len(map_data[0]): px = px_tmp
    if g.py < 0 or g.py >= len(map_data): g.py = py_tmp
    # 移動先が壁なら元の位置に戻す 
    mv = map_data[g.py][g.px]
    if mv == 1:
        g.px = px_tmp
        g.py = py_tmp
        # msgbox.showinfo(message="壁にぶつかった")
        return
    # プレイヤーを描画する --- (*10)
    canvas.delete("all")
    draw_map(canvas, map_data)
    draw_player(canvas)
    print(str(g.turn)+" player={0},{1}".format(g.px, g.py))
    # ゴールにたどり着いたか？
    if mv == 3:
        msgbox.showinfo(message="祝！ゴール！")



def move(movex, movey):
    px_tmp = g.px
    py_tmp = g.py
    xx, yy = [g.px * tile_size + 25, g.py * tile_size + 25]
    g.px += movex
    g.py += movey
    if g.px < 0 or g.px >= len(map_data[0]): px = px_tmp
    if g.py < 0 or g.py >= len(map_data): g.py = py_tmp
    # 移動先が壁なら元の位置に戻す 
    mv = map_data[g.py][g.px]
    if mv == 1:
        g.px = px_tmp
        g.py = py_tmp
        return
    # プレイヤーを描画する --- (*10)
    canvas.delete("all")
    draw_map(canvas, map_data)
    draw_player(canvas)
    if mv == 3:
        event_goal()


# ゴールイベント
def event_goal():
    init_env()

#----------------------------------


# 迷路データを取り込む --- (*1)
# def load_map_data():
#     from maze_data import data
#     return data

# 迷路を表示する関数 --- (*2)
def draw_map(cv, data):
    # 左上から右下へと描画
    rows = len(data)    # 迷路の行数
    cols = len(data[0]) # 迷路の列数
    for y in range(rows):
        y1 = y * tile_size
        y2 = y1 + tile_size
        for x in range(cols):
            x1 = x * tile_size
            x2 = x1 + tile_size
            # 該当場所の値を得る --- (*3)
            p = data[y][x]
            # 値に応じた色を決定する --- (*4)
            if p == 0: color = "white"
            if p == 1: color = "#404040"
            if p == 2: color = "red"
            if p == 3: color = "blue"
            # 正方形を描画 --- (*5)
            cv.create_rectangle(
                    x1, y1, x2, y2, # 座標
                    fill=color, # 塗色
                    outline="black", width=2) # 枠線
            if p == 1:
                draw_wall(cv, x1, y1)
            if p == 2:
                draw_waap(cv, x1, y1)
            if p == 3:
                draw_shiro(cv, x1, y1)
            if p == 0:
                draw_sougen(cv, x1, y1)



# 描画関連
def draw_wall(cv, x1, y1):
    cv.create_image(x1, y1, image=g.img_wall, anchor=NW)

def draw_steps(cv, x1, y1):
    cv.create_image(x1, y1, image=g.img_steps, anchor=NW)

def draw_waap(cv, x1, y1):
    cv.create_image(x1, y1, image=g.img_waap, anchor=NW)

def draw_sougen(cv, x1, y1):
    cv.create_image(x1, y1, image=g.img_sougen, anchor=NW)

def draw_renga(cv, x1, y1):
    cv.create_image(x1, y1, image=g.img_renga, anchor=NW)

def draw_shiro(cv, x1, y1):
    cv.create_image(x1, y1, image=g.img_shiro, anchor=NW)

def get_around_data():
    maplist = [map_data[g.py-1][g.px-1], map_data[g.py-1][g.px], map_data[g.py-1][g.px+1],
              map_data[g.py][g.px-1], map_data[g.py][g.px], map_data[g.py][g.px+1],
              map_data[g.py+1][g.px-1], map_data[g.py+1][g.px], map_data[g.py+1][g.px+1]
              ]
    return maplist


if __name__ == "__main__": main()
