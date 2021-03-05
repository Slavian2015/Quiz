from pymongo import MongoClient, ASCENDING, DESCENDING

client = MongoClient('mongodb_quiz', 27017)
db = client['QUIZ']
my_data = db['Data']

my_Personal = db['Personal']


def clean():
    my_Personal.remove({})
    my_data.remove({})


def insert_document(collection, data):
    return collection.insert_one(data).inserted_id


def update_document(collection, data, query):
    myquery = {"sku": query}
    newvalues = {"$set": {"sku": 1, "data": data}}
    return collection.update_one(myquery, newvalues)


def update_main_data(data=None):
    if not data:
        data = {
            "sku": 1,
            "data": {}
        }
    update_document(my_data, data, 1)
    return


def create_main_data():
    ls = ["Freedom",
          "Mastery",
          "Power",
          "Goal",
          "Curiosity",
          "Honor",
          "Acceptance",
          "Relatedness",
          "Order",
          "Status",
          ]

    old = []
    for i in ls:
        old.append(i)
        for k in ls:
            if k not in old:
                data = {"option1": i,
                        "option2": k}
                insert_document(my_data, data)


def get_list():
    d = []
    for i in my_data.find():
        d.append(i)
    return d


def add_person(mail):
    data = {
        "email": mail,
        "questions": {"test": "test"}
    }
    insert_document(my_Personal, data)


def get_all_personal():
    d = []
    for i in my_Personal.find():
        d.append(i["email"])
    return d


def insert_answer(btn1, btn2, answer, mail):
    myquery = {"email": mail}
    newvalues = {"$set": {f"questions.{btn1}_{btn2}": answer}}
    return my_Personal.update_one(myquery, newvalues)


def check_person(mail):
    for i in my_Personal.find({"email": mail}):
        return list(i["questions"].keys())





# clean()
# create_main_data()
# add_person("test@test.com")
# print(check_person("test@test.com"))




#
#
# print(get_list())
# for i in my_Personal.find({}):
#     print(i)
