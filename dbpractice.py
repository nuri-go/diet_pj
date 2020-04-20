from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('127.0.0.1', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.food


foodname = "갓김치"
food = db.food.find({'food_name':{'$regex':foodname}})

user = db.food.find_one({'food_name':foodname}, {'_id': 0 })
print (user)

for i in food:
    print("음식: "+str(i['food_name'] +' 용량: '+i['gram_foronetime']+' 칼로리: '+i['food_kcal']))



print (food)