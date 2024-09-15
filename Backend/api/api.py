import fastapi
from pydantic import BaseModel

app = fastapi.FastAPI()

class Patient(BaseModel):
    description: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/walkin/")
def walkin(patient: Patient):
    return {"description": patient.description}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)