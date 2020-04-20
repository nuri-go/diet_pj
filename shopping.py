from flask import Flask, render_template, jsonify, request
app = Flask(__name__, static_url_path='static')

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('127.0.0.1', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.food            # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('writekcal.html')

@app.route('/checkorder')
def show_table():
    return render_template('checkoder.html')

@app.route('/')
def main_get(num=None):
    return render_template('submit_test.html', num=num)

@app.route('/calculate', methods=['POST', 'GET'])
def calculate(num=None):
    ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
    ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
    if request.method == 'POST':
        #temp = request.form['num']
        pass
    elif request.method == 'GET':
        ## 넘겨받은 숫자
        temp = request.args.get('num')
        temp = str(temp)
        ## 넘겨받은 문자
        temp1 = request.args.get('char1')
        ## 넘겨받은 값을 원래 페이지로 리다이렉트
        return render_template('submit_test.html', num=temp, char1=temp1)
    ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함


## API 역할을 하는 부분
@app.route('/oderlist', methods=['POST'])
def make_order():
    user_name = request.form['ClientName']
    oder_amount = request.form['exampleFormControlSelect1']
    user_address = request.form['ClientAddr']
    user_callnumber = request.form['ClientTel']

    oder_list = {
        'user_name' : user_name,
        'oder_amount' : oder_amount,
        'user_address' : user_address,
        'user_callnumber': user_callnumber
            }
    db.dbhomework.insert_one(oder_list)
    return jsonify({'result':'success', 'msg': '주문이 성공적으로 이루어졌습니다'})

@app.route('/oderlist', methods=['GET'])
def read_order():
    oderfromUser = list(db.dbhomework.find({},{'_id':0}))
    return jsonify({'result': 'success', 'oder': oderfromUser})

@app.route('/search', methods=['GET'])
def search():
    print('지금 되고있는거니..?')
    food_name = request.args.get('foodname')

    print('안되는거지?')
    print(food_name)

    foodkcal = list(db.food.find({'food_name': {'$regex': food_name}}))

    for i in foodkcal:
       print("음식: " + str(i['food_name'] + ' 용량: ' + i['gram_foronetime'] + ' 칼로리: ' + i['food_kcal']))
    return jsonify({'result':'success', 'food':foodkcal })

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
