from fastapi import FastAPI
from pydantic import BaseModel
from cache import MyCache
from distributed import MyDistributed
from datetime import datetime

app = FastAPI()
pets = MyCache()
pets_distributed = MyDistributed(pets)

class PetEntity(BaseModel):
    name: str
    kind: str

@app.get("/")
def get_index():
    return "Please go to http://localhost:8000/docs"

@app.get("/pets")
def get_pets():
    return pets.keys()

@app.post("/pet")
def post_pet(pet: PetEntity):
    pets.set(pet.name, pet)

@app.get("/pet")
def get_pet(name: str):
    return pets.get(name)

pets_distributed.expose_to_fastapi('/pets', app)
