import os
import sys

class Common:
    
    def setfolder(self):
        #pyinstallerで作るときはこちらを有効
        print("sys.executable= "+sys.executable)
        dirname = os.path.dirname(sys.executable)
        print("sys.executable(dir)= "+dirname)
        os.chdir(dirname) # カレントディレクトリを移動する

        #普通にVisualStudioCodeなどで実行するときはこちらを有効に
        print(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # カレントディレクトリを移動する
