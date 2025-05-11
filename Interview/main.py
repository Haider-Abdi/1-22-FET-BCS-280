from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List,Optional
from uuid import uuid4
import requests

app = FastAPI()
transactions ={}

class Transaction(BaseModel):
    id:Optional[str] = None
    date:str
    category:str
    subcategory:str
    amount:float
    description:str

@app.post("/transactions",response_model = Transaction)
def create_transaction(txn:Transaction):
    txn.id = str(uuid4())
    transactions[txn.id]=txn
    return txn

@app.get("/transactions",response_model=List[Transaction])
def get_all_transactions():
    total_amount = sum(t.amount for t in transactions)
    return {
        "transactions":[{"date":t.date,"amount":t.amount} for t in transactions],
        "total_amount":total_amount
    }

@app.get("/transactions/category/{category}")
def get_by_category(category:str):
    filtered = [t for t in transactions if t.category.lower() == category.lower()]
    return {
        "transactions":filtered,"total_amount":sum(t.amount for t in filtered)
    }

@app.get("/transactions/subcategory/{subcategory}")
def get_by_subcategory(subcategory:str):
    filtered = [t for t in transactions if t.subcategory.lower() == subcategory.lower()]
    return {
        "transactions":filtered,"total_amount":sum(t.amount for t in filtered)
    }

@app.put("/transaction/{txn_id}",response_model=Transaction)
def update_transaction(txn_id:str,updated:Transaction):
    for i,txn in enumerate(transactions):
        if txn.id ==txn_id:
            transactions[i] = updated
            return updated
    raise HTTPException(status_code=404,detail="Transaction not found")

@app.delete("/transactions/{txn_id}")
def delete_transaction(txn_id:str):
    global transactions
    transactions = [t for t in transaction if t.id != txn_id]
    return {
        "message":"Transaction deleted"
    }

# data = {
#     "date": "06-01-2022",
#     "category": "Food",
#     "subcategory": "Groceries",
#     "amount": 50.5,
#     "description" : "Pizza",
# }
# res = requests.post("http://127.0.0.1:8000/transactions",json = data)
# print(res.json)