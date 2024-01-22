
import os
import sqlite3
import pandas as pd

dbname = 'db_test.db'      #作成するデータベース
csvfilename = 'dummy.csv' #読み込むCSVファイル名

class flask_sqlite:
    def init(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__))) # カレントディレクトリを移動する
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()


    #テーブル削除
    def delete_table(self):
        self.cur.execute('DROP TABLE IF EXISTS persons')


    #テーブル作成
    def create_table(self):
        self.cur.execute('CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')


    #データ挿入
    def insert_data(self):
        self.cur.execute('INSERT INTO persons(name) values("Sato")')
        self.cur.execute('INSERT INTO persons(name) values("Suzuki")')
        self.cur.execute('INSERT INTO persons(name) values("Takahashi")')

        self.cur.execute('select * from persons')

        list1 = self.cur.fetchall()
        for l in list1:
            print(l)

        self.conn.commit()


    #クローズ
    def close_table(self):
        self.cur.close()
        self.conn.close()

    #一連のセット
    def first(self):
        self.init()
        self.delete_table()
        self.create_table()
        self.insert_data()
        self.close_table()


    #全件検索
    def select_all(self):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        self.cur.execute('select * from persons')
        persons = self.cur.fetchall()
        # for l in persons:
        #     print(l)
        return persons


    #検索
    def select_word(self, word):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        sql = 'select * from persons where "氏名" = "' + word + '"'

        print(sql)
        self.cur.execute(sql)
        persons = self.cur.fetchall()
        # for l in persons:
        #     print(l)
        return persons


    #一行取得
    def select_one(self, id):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.execute('select * from persons where id = ' + str(id))
        person = self.cur.fetchone()
        print("person=",person)
        return person


    #最大IDの取得
    def select_max_id(self):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.execute('select max(id) as id from persons')
        max = self.cur.fetchone()
        print("max=",max[0])
        print(type(max[0]))
        return max[0]


    #CSVファイルからの読み込み
    def insert_db_from_excel(self):
        # CSVファイルの読み込んで変数に代入する
        df_csv = pd.read_csv(csvfilename, encoding = 'utf-8')  # 文字コードはshift-jisやutf-8など
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        df_csv.to_sql('persons', self.conn, if_exists='replace',index_label='id') # 最初の引数はテーブル名、if_existsは同じテーブル名が存在する場合の動作を指定している(append,replace,failがある) 
        self.conn.close()


    #カラム名称の取得
    def get_column_name(self):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        # カラム情報を取得するSQLクエリ
        table_name = 'persons'
        get_column_info_query = f"PRAGMA table_info({table_name})"
        # SQLクエリを実行
        self.cur.execute(get_column_info_query)
        # カラム情報を取得し、カラム名を抽出
        column_info = self.cur.fetchall()
        column_names = [column[1] for column in column_info]
        # カラム名を表示
        # for column_name in column_names:
        #     print(column_name)
        self.conn.close() 
        return column_names        


    #カラム数の取得
    def get_column_count(self):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        # カラム情報を取得するSQLクエリ
        table_name = 'persons'
        get_column_info_query = f"PRAGMA table_info({table_name})"
        # SQLクエリを実行
        self.cur.execute(get_column_info_query)
        # カラム情報を取得し、カラム名を抽出
        column_info = self.cur.fetchall()
        column_names = [column[1] for column in column_info]
        # 接続を閉じる
        self.conn.close()
 
        return len(column_names)     
    

    #データ登録
    def regist_data(self, columns, datas):

        maxid = self.select_max_id()
        maxid += 1
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        sql = 'INSERT INTO persons('
        sql = sql +"'"+ columns[0] + "'"
        for num in range(1, len(columns)):
            sql = sql +",'"+ columns[num] + "'"
            # print(columns[num], datas[num])
        sql = sql + ") VALUES("
        sql = sql +"'"+ str(maxid) + "'"
        for num in range(1, len(columns)):
            sql = sql +",'"+ datas[num] + "'"
        sql = sql + ")"
        print(sql)

        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()   # 接続を閉じる


    
    def update_data(self, columns, datas):
        maxid = self.select_max_id()
        maxid += 1

        # dbname = 'db_test.db'
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        sql = 'UPDATE persons SET '
        sql = sql +"'"+ columns[1] + "'='"+datas[1] + "'"
        for num in range(2, len(columns)):
            sql = sql +",'"+ columns[num] + "'='" + datas[num] + "'"
        sql = sql + " where id = " + datas[0]
        print(sql)

        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()   # 接続を閉じる

    #入力サンプル
    # select * from persons where "氏名" = "山田 太郎" という形で検索する
    # sql = 'select * from persons where "氏名" = "' + word + '"'
    # sql = 'select * from persons where "氏名" like "%' + word + '%"'
    # sql = 'select * from persons where "氏名" like "%' + word + '%" OR "氏名（ひらがな）" like "%'+ word + '%"'
