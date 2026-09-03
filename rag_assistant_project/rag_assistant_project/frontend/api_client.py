import os, requests
from dotenv import load_dotenv
load_dotenv(); BASE=os.getenv("API_BASE_URL","http://localhost:8000")
def ask(question):
    r=requests.post(f"{BASE}/query",json={"question":question},timeout=120); r.raise_for_status(); return r.json()
