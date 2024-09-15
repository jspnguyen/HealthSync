from fastapi import WebSocket
import fastapi
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append("..")
import main
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

class Counts(BaseModel):
    total_doctors: int
    available_doctors: int
    total_nurses: int
    available_nurses: int
    total_equipment: int
    available_equipment: int
    patients_being_treated: int
    patients_in_waiting_room: int
    beds_available: int


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/walkin/")
def walkin(patient: Patient):
    json = patient.model_dump()
    with open("json/patients.json", "w") as f:
        f.write(str(json).replace("'", "\""))
    return {"Status": "Success"}

@app.post("/counts/")
def walkin(counts: Counts):
    json = counts.model_dump()
    with open("json/counts.json", "w") as f:
        f.write(str(json).replace("'", "\""))
    return {"Status": "Success"}

@app.get("/graph")
def get_graph():
    with open("./json/graph.json", 'r') as f:
        graph = json.load(f)
    return graph

@app.get("/allcounts")
def get_allcounts():
    with open("./json/counts.json", 'r') as f:
        counts = json.load(f)
    return counts




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)