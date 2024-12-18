import json


def read_data():
    with open("./app/data.json", "r") as f:
        data = json.load(f)
    return data


def get_mutual_funds(fund_type):
    data = read_data()
    print(data)
    return data[fund_type]
