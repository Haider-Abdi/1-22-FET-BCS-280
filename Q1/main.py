from fastapi import FastAPI, Path, HTTPException
from typing import Dict, List
import httpx
import asyncio
import os
from dotenv import load_dotenv  

load_dotenv()

app = FastAPI()


WINDOW_SIZE = 10
number_windows = {
    'p': [],  
    'f': [],  
    'e': [],  
    'r': []   
}


API_URLS = {
    'p': 'http://20.244.56.144/evaluation-service/primes',
    'f': 'http://20.244.56.144/evaluation-service/fibo',
    'e': 'http://20.244.56.144/evaluation-service/even',
    'r': 'http://20.244.56.144/evaluation-service/rand',
}


BEARER_TOKEN = os.getenv("BEARER_TOKEN")

if not BEARER_TOKEN:
    raise RuntimeError("BEARER_TOKEN is missing in .env file")

async def fetch_numbers_from_api(numberid: str) -> List[int]:
    url = API_URLS[numberid]
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            resp = await client.get(url, headers=headers)
            print(f"Requested {url}")
            print(f"Status code: {resp.status_code}")
            print(f"Response text: {resp.text}")
            resp.raise_for_status()
            data = resp.json()
            return data.get("numbers", [])
    except Exception as e:
        print(f"Error fetching numbers: {e}")
        return []

@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str = Path(..., regex="^[pfer]$")) -> Dict:
    prev_state = number_windows[numberid].copy()
    numbers = await fetch_numbers_from_api(numberid)
    
    for num in numbers:
        if num not in number_windows[numberid]:
            number_windows[numberid].append(num)
            if len(number_windows[numberid]) > WINDOW_SIZE:
                number_windows[numberid].pop(0)
    curr_state = number_windows[numberid].copy()
    avg = round(sum(curr_state) / len(curr_state), 2) if curr_state else 0.0
    return {
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": numbers,
        "avg": avg
    } 

