from fastapi import WebSocket
import fastapi
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append("..")
import main
import hashlib
import asyncio
import json
import time



app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Patient(BaseModel):
    description: str



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/walkin/")
def walkin(patient: Patient):
    json = patient.model_dump()
    with open("json/patients.json", "w") as f:
        f.write(str(json).replace("'", "\""))
    return {"Status": "Success"}

@app.get("/graph")
def get_graph():
    with open("./json/graph.json", 'r') as f:
        graph = json.load(f)
    return graph

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)