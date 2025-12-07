from fastapi import FastAPI
from core.verification_engine import verify_person

app = FastAPI()

@app.get("/verify")
def verify(name: str, npi: str = None):
    return verify_person(name, npi)
