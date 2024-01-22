from flask import Flask, request, render_template
import flask_common
import flask_sqlite

#フォルダ設定
common = flask_common.Common()
common.setfolder()#フォルダ設定
sqlite = flask_sqlite.flask_sqlite()

sqlite.init()
sqlite.delete_table()           #これをコメントするとCSVから読まなくなる。
sqlite.insert_db_from_excel()   #これをコメントするとCSVから読まなくなる。

# sqlite.select_all()             #全件取得テスト
# sqlite.get_column_name()      #テスト
# sqlite.select_max_id()        #テスト

app = Flask(__name__, static_folder='.', static_url_path='')

#ホームページ表示(index.html)
@app.route('/')
def index():
    return app.send_static_file('templates/home.html')


# データの登録
@app.route('/registproc', methods=['GET'])
def regist_proc():
    columncou = sqlite.get_column_count()
    print("columncou", columncou)
    datas = []
    for num in range(columncou):
        tag_name = "data"+str(num)
        print(tag_name)
        # data = request.form.get(tag_name)
        data = request.args.get(tag_name)
        print(data)
        datas.append(data)
    print(datas)

    columns = sqlite.get_column_name()

    sqlite.regist_data(columns, datas)#データ登録

    list = sqlite.select_all()
    return render_template('main.html', results= list )


# データの登録
@app.route('/editproc', methods=['GET'])
def edit_proc():
    columncou = sqlite.get_column_count()
    print("columncou", columncou)
    datas = []
    for num in range(columncou):
        tag_name = "data"+str(num)
        print(tag_name)
        # data = request.form.get(tag_name)
        data = request.args.get(tag_name)
        print(data)
        datas.append(data)
    print(datas)

    columns = sqlite.get_column_name()

    sqlite.update_data(columns, datas)#データ登録

    list = sqlite.select_all()
    return render_template('main.html', results= list )


# データの検索
@app.route('/searchproc', methods=['GET'])
def search_proc():
    data = request.args.get("searchword")
    print(data)

    list = sqlite.select_word(data)
    return render_template('search.html', results= list )



@app.route('/main', methods=['GET'])
def main_form():
    list = sqlite.select_all()
    return render_template('main.html', results= list )

@app.route('/input', methods=['GET'])
def input_form():
    columns = sqlite.get_column_name()
    return render_template('input.html', columns= columns  )

@app.route('/search', methods=['GET'])
def search_form():
    # columns = sqlite.get_column_name()
    return render_template('search.html' )



@app.route('/edit', methods=['GET'])
def edit_form():
    columns = sqlite.get_column_name()
    id = request.args.get('id')
    print("id=",id)
    person = sqlite.select_one(id)
    print("person",person)
    return render_template('edit.html', person= person, columns= columns  )



@app.route('/contact', methods=['GET'])
def contact_form():
    # columns = sqlite.get_column_name()
    return render_template('contact.html')
                           

@app.route('/notyet', methods=['GET'])
def notyet_form():
    return render_template('notyet.html', results= list )

@app.route('/detail', methods=['GET'])
def detail_form():
    id = request.args.get('id')
    print("id=",id)
    person = sqlite.select_one(id)
    print("person",person)
    # req = request.args
    # user_id = req.get("id")
    # print("user_id=",user_id)
    columns = sqlite.get_column_name()

    return render_template('detail.html', person= person, columns= columns )

# app.run(debug=True)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
