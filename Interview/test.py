import requests

data = {
    "date": "06-01-2022",
    "category": "Food",
    "subcategory": "Groceries",
    "amount": 50.5,
    "description" : "Pizza",
}
res = requests.post("http://127.0.0.1:8000/transactions",json = data)
print(res.json)