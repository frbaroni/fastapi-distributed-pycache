from fastapi import FastAPI
from pydantic import BaseModel
from cache import MyCache

app = FastAPI()
pets = MyCache()

class PetEntity(BaseModel):
    name: str
    kind: str

@app.get("/")
def get_index():
    return "Please go to http://localhost:8000/docs"

@app.post("/pet")
def post_pet(pet: PetEntity):
    pets.set(pet.name, pet)

@app.get("/pet")
def get_pet(name: str):
    return pets.get(name)
