import pyxel
import random
import numpy as np
import time

# pyxel.blt(50, 50, 0, 0, 0, 8, 8, 0)
# 画面の（50，50）の位置にイメージバンク「0」の（0，0）の位置から横8、縦8の範囲を描画し、
# カラーコード「0」（黒）は透過させる。


class MazeEnv:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 上、下、左、右
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.2
        self.episode = 0
        self.training = True
        self.goal = (8, 8)
        self.tsize = 8
        self.walls = [(random.randint(1, 8), random.randint(1, 8)) for _ in range(15)]
        print(self.walls)
        self.reset()
        self.steps = []  # AIの動きを記録するリスト

    def reset(self):
        self.player = (1, 1)
        self.steps = [self.player]  # 初期位置を追加
        return self.player

    def step(self, action):
        new_x = self.player[0] + action[0]
        new_y = self.player[1] + action[1]

        if (0 <= new_x < self.width and 0 <= new_y < self.height and (new_x, new_y) not in self.walls):
            self.player = (new_x, new_y)
            self.steps.append(self.player)  # 移動後の位置を記録

        reward = -1 #ステップごとに-1していく
        done = False
        if self.player == self.goal: #ゴールについたら１００ポイント
            reward = 100
            done = True

        return self.player, reward, done

    def render(self):
        pyxel.cls(0)

        # 壁の描画
        for x in range(self.width):
            for y in range(self.height):
                # pyxel.rect(x * 10, y * 10, 10, 10, 7 if (x, y) in self.walls else 0)

                # print(x, y)
                if  (x, y) in self.walls:
                    pyxel.blt(x * self.tsize, y * self.tsize, 0, self.tsize*1, 0, self.tsize, self.tsize, 0)  # enemy.png を表示
                else:
                    pyxel.rect(x * self.tsize, y * self.tsize, self.tsize, self.tsize, 0)


                # pyxel.blt(50, 50, 0, 0, 0, 8, 8, 0)
                # 画面の（50，50）の位置にイメージバンク「0」の（0，0）の位置から横8、縦8の範囲を描画し、
                # カラーコード「0」（黒）は透過させる。
                # pyxel.blt(x * 10, y * 10, 0, 0, 0, 8, 8, 0)  # enemy.png を表示
 

        # ゴールの描画
        pyxel.rect(self.goal[0] * self.tsize, self.goal[1] * self.tsize, self.tsize, self.tsize, 11)

        # AIの移動軌跡を表示
        bcou = 0
        for step in self.steps:
            # pyxel.rect(step[0] * self.tsize, step[1] * self.tsize, self.tsize, self.tsize, 5)
            pyxel.blt(step[0] * self.tsize, step[1] * self.tsize, 0, self.tsize*0, 0, self.tsize, self.tsize, 0) 

            pyxel.flip()  # 描画を更新
            # pyxel.rect(step[0] * self.tsize, step[1] * self.tsize, self.tsize, self.tsize, 6)
            pyxel.blt(step[0] * self.tsize, step[1] * self.tsize, 0, self.tsize*3, 0, self.tsize, self.tsize, 1) 


            if(self.episode==1):
                if(bcou < 50):
                    time.sleep(0.5)
                elif(bcou <100):
                    time.sleep(0.25)
                elif(bcou <150):
                    time.sleep(0.20)
                elif(bcou <200):
                    time.sleep(0.10)
                else:
                    time.sleep(0.001)

            bcou=bcou+1

        # プレイヤーの描画
        pyxel.rect(self.player[0] * self.tsize, self.player[1] * self.tsize, self.tsize, self.tsize, 9)
        # pyxel.blt(self.player[0] * self.tsize, self.player[1] * self.tsize, 0, self.tsize*0, 0, self.tsize, self.tsize, 0) 
        pyxel.text(5, 5, f"Episode: {self.episode}", 7)
        # pyxel.text(5, 15, f"Training: {self.training}", 7)

        pyxel.flip()  # 描画を更新

        time.sleep(1)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return max(self.actions, key=lambda a: self.q_table.get((state, a), 0))

    def update_q_table(self, state, action, reward, next_state):
        max_next_q = max([self.q_table.get((next_state, a), 0) for a in self.actions])
        current_q = self.q_table.get((state, action), 0)
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def train_step(self):
        state = self.reset()
        done = False
        while not done:
            action = self.choose_action(state)
            next_state, reward, done = self.step(action)
            self.update_q_table(state, action, reward, next_state)
            state = next_state
        self.episode += 1
        if self.episode >= 500:
            self.training = False

if __name__ == "__main__":
    env = MazeEnv()
    # pyxel.init(80, 80, title="Maze AI", display_scale=3)
    pyxel.init(80, 80, title="Maze AI")
    pyxel.load("assets.pyxres")  # 画像ファイルを読み込む

    def update():
        if env.training:
            env.train_step()

    def draw():
        env.render()

    pyxel.run(update, draw)