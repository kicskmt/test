import PIL.Image
import PIL.ImageTk
import tkinter.messagebox as msgbox
import random
import global_value as g
from tkinter import *
from neural_network_mlp import *
import time


movetime = 1 
maxturn = 100 #最大ターン数
nncou = 40 #作成するNNの数

iconicmode = False #ウィンドウをアイコン化して起動
wallmode = False  #壁を草原にする
stopflg = False
prtmode = False

# tile_size = 25 # 描画タイルのサイズ
tile_size = 50 # 描画タイルのサイズ

block_percent = 5 #ブロックを増やす割合

# グローバル変数の初期化
g.px = 2
g.py = 2

player_image = "icons\icon_robot_red.png" # プレイヤーの画像ファイル
# player_image = "icons\icon_robot_red_25.png" # プレイヤーの画像ファイル

iconfile_wall = "icons\icon_wall.png"
iconfile_steps = "icons\icon_steps.png"
iconfile_sougen = "icons\icon_sougen.png"
iconfile_sougen2 = "icons\icon_sougen2.png"
iconfile_robot = "icons\icon_robot_red.png"
iconfile_renga = "icons\icon_renga.png"
iconfile_shiro = "icons\icon_shiro2.png"

map_file = "maze5.tsv"

# プレイヤーの画像を読み込む --- (*3)
def load_wall(cv):
    g.img_wall = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_wall))
    # g.img_steps = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_steps))
    g.img_sougen = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_sougen))
    g.img_renga = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_renga))
    g.img_shiro = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_shiro))

    if wallmode == True:
        g.img_wall = PIL.ImageTk.PhotoImage(PIL.Image.open(iconfile_sougen2))


def main():
    global map_data
    # 迷路データを読み込む
    #★★★★下を修正★★★★★
    map_data = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    map_data = load_map(map_file)

    #ブロックを増やすとき
    add_block_map()

    # NNを作る
    g.turn = 0
    create_nn()
    # ウィンドウを作成 --- (*2)
    #★★★★下を修正★★★★★
    create_window(map_data, [load_image, set_event])
    # create_window(map_data, [load_image])
    # create_window(map_data, [])
    


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

    if iconicmode == True:
        g.win.state('iconic')

    #★★★★下を修正★★★★★
    g.win.after(movetime, change_label_text,) 

    # 追加処理があればここで処理する --- (*7)
    for func in events: func(g.cv, map_data)
    g.win.mainloop()



def change_label_text():
    if stopflg == True:
        return
    #100ms後にchange_label_textを実行
    g.turn = g.turn + 1
    g.win.title("迷路 "+ "generation:"+ str(g.generation)+" NN:"+str(g.nn_using) + " ステップ:"+str(g.turn))

    if(g.turn > maxturn):
        g.nn.fitness = calc_distance_goal()
        if prtmode:
            print("generation:"+ str(g.generation)+" NN:"+str(g.nn_using) + " ステップ:"+str(g.turn) + " fitness:"+str(g.nn.fitness))
        init_env()

    ret = run_nn()
    ran = round(ret/0.25)

    #★★★★下を修正★★★★★
    # ran = random.randint(1, 4)

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


#移動処理
def move(movex, movey):
    px_tmp = g.px
    py_tmp = g.py
    xx, yy = [g.px * tile_size + 25, g.py * tile_size + 25]
    g.px += movex
    g.py += movey
    if g.px < 0 or g.px >= len(map_data[0]): px = px_tmp
    if g.py < 0 or g.py >= len(map_data): g.py = py_tmp
    mv = map_data[g.py][g.px]
    if prtmode:
        print(mv, end="")
    if mv == 1:
        g.px = px_tmp
        g.py = py_tmp
        return
    # プレイヤーを描画する --- (*10)
    #★★★★下を修正★★★★★
    # canvas.delete("all")
    # draw_map(canvas, map_data)
    draw_player(canvas)
    # ゴールにたどり着いたか？
    if mv == 3:
        event_goal()


def calc_distance_goal():
    distance = (24-g.px)+(18-g.py)
    if prtmode:
        print("(" +str(g.px) +"," + str(g.py) + ")distance=" + str(distance))
    return distance


def create_nn():
    g.nnall = []
    
    for i in range(nncou):
        g.nnall.append(NeuralNetwork())
        
    # #0番目を設定
    g.nn_using = -1
    g.nn = g.nnall[g.nn_using]
    g.generation = 0


def init_env():
    stopflg = True
    g.nn_using = g.nn_using + 1
    if g.nn_using >= nncou-1:
        event_generation()
    g.nn = g.nnall[g.nn_using]
    g.px = 2
    g.py = 2
    g.turn = 0
    canvas.delete("all")
    draw_map(canvas, map_data)
    draw_player(canvas)
    stopflg = False


def event_generation():
    g.generation = g.generation + 1
    if prtmode:
        print("\n" + str(g.generation) +"世代 ソート前 ", end='' )
        for i in range(nncou):
            print(str(g.nnall[i].fitness), end=' , ' )
    #ソート
    for i in range(nncou):
        for j in range(i+1, nncou):
            if g.nnall[i].fitness > g.nnall[j].fitness:
                nntmp = g.nnall[i]
                g.nnall[i] = g.nnall[j]
                g.nnall[j] = nntmp
    if prtmode:
        print("\n"+ str(g.generation) +"世代 ソート後 ", end='' )
        for i in range(nncou):
            print(str(g.nnall[i].fitness) , end=' , ')

    smartnum = 0
    for i in range(nncou):
        print(g.nnall[i].fitness, end=",")
        if(g.nnall[i].fitness > 1):
            break
        smartnum = smartnum + 1


    #crossover & mutation
    # for i in range(1, nncou-10):
    #     g.nnall[i+10].nn_crossover2(g.nnall[1], g.nnall[i])
    #     g.nnall[i+10].nn_mutation()
    for i in range(1, nncou-smartnum):
        g.nnall[i+smartnum].nn_crossover2(g.nnall[1], g.nnall[i])
        g.nnall[i+smartnum].nn_mutation()
    #NNの使用番号初期化
    g.nn_using = 0
    if prtmode:
        print("")


def run_nn():
    # 実行
    input_data = get_around_data()
    ret = g.nn.commit(input_data) 
    # print(ret)
    return ret


# CSV(タブ区切り)を読み込む
def load_map(filename):
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


def add_block_map():
    gyou = len(map_data)
    retu = len(map_data[0])
    print(gyou)
    print(retu)

    for i in range(gyou):
        for j in range(retu):
            if map_data[i][j] == 0:
                ran = random.randint(1, 100)
                if ran < block_percent:
                    map_data[i][j] = int(1)
            print(map_data[i][j], end = "")
        print("") 

    print("add_block_map finished")



# プレイヤー画像読み込み
def load_image(cv, map_data):
    global canvas, img_tk
    canvas = cv
    img = PIL.Image.open(player_image)
    img_tk = PIL.ImageTk.PhotoImage(img)
    draw_player(canvas)

# プレイヤー描画
def draw_player(cv):
    x = g.px * tile_size
    y = g.py * tile_size
    cv.create_image(x, y, image=img_tk, anchor=NW)

# マウスイベント
def set_event(cv, maze_data):
    cv.bind("<1>", canvas_click)

# キャンバスクリック
def canvas_click(e):
    mx = e.x # マウスのX座標
    my = e.y # マウスのY座標
    px_tmp = g.px
    py_tmp = g.py
    xx, yy = [g.px * tile_size + 25, g.py * tile_size + 25]
    ix = mx - xx
    iy = my - yy
    if abs(ix) > abs(iy): # 左右移動
        if ix > 0: g.px += 1
        else: g.px -= 1
    else: # 上下移動
        if iy > 0: g.py += 1
        else: g.py -= 1
    if g.px < 0 or g.px >= len(map_data[0]): g.__annotations__px = px_tmp
    if g.py < 0 or g.py >= len(map_data): g.py = py_tmp
    mv = map_data[g.py][g.px]
    if mv == 1:
        g.px = px_tmp
        g.py = py_tmp
        return
    canvas.delete("all")
    draw_map(canvas, map_data)
    draw_player(canvas)
    if prtmode == True:
        print(str(g.turn)+" player={0},{1}".format(g.px, g.py))
    # ゴールにたどり着いたか？
    if mv == 3:
        msgbox.showinfo(message="祝！ゴール！")



# ゴールイベント
def event_goal():
    g.nn.nn_save("nn")
    # g.nn.nn_load()
    g.nn.fitness = calc_distance_goal()
    print("generation:"+ str(g.generation)+" NN:"+str(g.nn_using) + " ステップ:"+str(g.turn) + " fitness:"+str(g.nn.fitness))
    init_env()

#----------------------------------


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
            #★★★★下を修正★★★★★
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
