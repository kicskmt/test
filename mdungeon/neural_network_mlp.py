import numpy as np
# import matplotlib.pyplot as plt
# from sklearn import datasets
import random
import csv
import maze_play_ai3
import json
from copy import deepcopy

input_cou = 9
middle_cou = 9
output_cou = 1

nn_file = "nn_file.csv"


# シグモイド関数
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# ニューロン
class Neuron:
    def __init__(self):  # 初期設定
        self.input_sum = 0.0
        self.output = 0.0

    def set_input(self, inp):
        self.input_sum += inp

    def get_output(self):
        self.output = sigmoid(self.input_sum)
        return self.output

    def reset(self):
        self.input_sum = 0
        self.output = 0

# ニューラルネットワーク
class NeuralNetwork:
    def __init__(self):  # 初期設定

        # 重み
        self.w_im = []
        for i in range(middle_cou):
            tmp = []
            for j in range(input_cou):
                tmp.append(random.random()-0.5)
            self.w_im.append(tmp)

        self.w_mo = []
        for i in range(output_cou):
            tmp = []
            for j in range(middle_cou):
                tmp.append(random.random()-0.5)
            self.w_mo.append(tmp)

        self.b_m = []
        self.b_o = []

        for i in range(middle_cou):
            self.b_m.append(random.random())

        for i in range(output_cou):
            self.b_o.append(random.random())

        self.input_layer = []
        self.middle_layer = []
        self.output_layer = []

        for i in range(input_cou):
            self.input_layer.append(0.0)

        for i in range(middle_cou):
            self.middle_layer.append(Neuron())

        for i in range(output_cou):
            self.output_layer.append(Neuron())




    def commit(self, input_data):  # 実行
        for i in range(input_cou):
            # self.input_layer[i].reset()
            self.input_layer[i] = input_data[i]

        for i in range(middle_cou):
            self.middle_layer[i].reset()
        
        for i in range(output_cou):
            self.output_layer[i].reset()

        for i in range(middle_cou):
            for j in range(input_cou):
                # print("i="+str(i)+"j="+str(j))
                self.middle_layer[i].set_input(self.input_layer[j] * self.w_im[i][j])
            self.middle_layer[i].set_input(self.b_m[i])

        for i in range(output_cou):
            for j in range(middle_cou):
                self.output_layer[i].set_input(self.middle_layer[i].get_output() * self.w_mo[i][j])
            self.output_layer[i].set_input(self.b_o[i])

        return self.output_layer[0].get_output()

    def nn_save(self):

        csvfile = open("nn.csv","w")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(self.w_im)
        csvwriter.writerows(self.w_mo)
        csvwriter.writerow(self.b_m)
        csvwriter.writerow(self.b_o)
        csvfile.close()

        dic_nn = {"w_im":self.w_im, "w_mo":self.w_mo, "b_m":self.b_m, "b_o":self.b_o}

        jsonfile = open("nn.json","w")
        json.dump(dic_nn, jsonfile, indent=4)
        jsonfile.close()


    def nn_save(self, name):

        dic_nn = {"w_im":self.w_im, "w_mo":self.w_mo, "b_m":self.b_m, "b_o":self.b_o}

        jsonfile = open(""+ name +".json","w")
        json.dump(dic_nn, jsonfile, indent=4)
        jsonfile.close()


    def nn_load(self):
            jsonfile = open("nn.json","r")
            dic_nn = json.load(jsonfile)
            jsonfile.close()
            print("読み込み前")
            print(self.w_im)
            self.w_im = dic_nn["w_im"]
            self.w_mo = dic_nn["w_mo"]
            self.b_m = dic_nn["b_m"]
            self.b_o = dic_nn["b_o"]



            print("読み込み後")
            print(self.w_im)
            print(self.w_mo)
            print(self.b_m)
            print(self.b_o)



    def nn_load(self, name):
            jsonfile = open(""+ name +".json","r")
            dic_nn = json.load(jsonfile)
            jsonfile.close()
            print("読み込み前")
            print(self.w_im)
            self.w_im = dic_nn["w_im"]
            self.w_mo = dic_nn["w_mo"]
            self.b_m = dic_nn["b_m"]
            self.b_o = dic_nn["b_o"]




    def nn_crossover(self, NN1, NN2):
        # self.print_nn()
        ran = random.randint(1,4)
        if ran == 1:
            self.w_im = deepcopy(NN1.w_im)
            self.w_mo = deepcopy(NN1.w_mo)
            self.b_m = deepcopy(NN1.b_m)
            self.b_o = deepcopy(NN2.b_o)
        elif ran == 2:
            self.w_im = deepcopy(NN1.w_im)
            self.w_mo = deepcopy(NN1.w_mo)
            self.b_m = deepcopy(NN2.b_m)
            self.b_o = deepcopy(NN2.b_o)
        elif ran == 3:
            self.w_im = deepcopy(NN1.w_im)
            self.w_mo = deepcopy(NN2.w_mo)
            self.b_m = deepcopy(NN2.b_m)
            self.b_o = deepcopy(NN2.b_o)
        elif ran == 4:
            self.w_im = deepcopy(NN1.w_im)
            self.w_mo = deepcopy(NN1.w_mo)
            self.b_m = deepcopy(NN1.b_m)
            self.b_o = deepcopy(NN2.b_o)
        # self.print_nn()

    def nn_crossover2(self, NN1, NN2):
        ran = random.randint(1,middle_cou*input_cou)
        cou = 0
        for i in range(middle_cou):
            for j in range(input_cou):
                if cou < ran:
                    self.w_im[i][j] = NN1.w_im[i][j]
                else:
                    self.w_im[i][j] = NN2.w_im[i][j]
                cou = cou+1

        ran = random.randint(1,output_cou*middle_cou)
        cou = 0
        for i in range(output_cou):
            for j in range(middle_cou):
                if cou < ran:
                    self.w_mo[i][j] = NN1.w_mo[i][j]
                else:
                    self.w_mo[i][j] = NN2.w_mo[i][j]
                cou = cou+1

        ran = random.randint(1,middle_cou)
        cou = 0
        for i in range(middle_cou):
            if cou < ran:
                self.b_m[i] = NN1.b_m[i]
            else:
                self.b_m[i] = NN2.b_m[i]
            cou = cou+1


        ran = random.randint(1,output_cou)
        cou = 0
        for i in range(output_cou):
            if cou < ran:
                self.b_o[i] = NN1.b_o[i]
            else:
                self.b_o[i] = NN2.b_o[i]
            cou = cou+1





    def print_nn(self):
        tmp = 0
        for i in range(middle_cou):
            for j in range(input_cou):
                tmp = tmp + self.w_im[i][j]
        for i in range(output_cou):
            for j in range(middle_cou):
                tmp = tmp + self.w_mo[i][j]
        for i in range(middle_cou):
            tmp = tmp + self.b_m[i]
        for i in range(output_cou):
            tmp = tmp + self.b_o[i]
        print(tmp , end=" ")

            
    def nn_mutation(self):
        # ran = random.randint(1,4)

        for i in range(middle_cou):
            for j in range(input_cou):
                if random.randint(1,5)==1:
                   self.w_im[i][j] = random.random()-0.5

        for i in range(output_cou):
            for j in range(middle_cou):
                if random.randint(1,5)==1:
                    self.w_mo[i][j] = random.random()-0.5

        for i in range(middle_cou):
            if random.randint(1,5)==1:
                self.b_m[i]=random.random()

        for i in range(output_cou-1):
            if random.randint(1,5)==1:
                self.b_o[i]=random.random()





if __name__ == "__main__": maze_play_ai3.main()

