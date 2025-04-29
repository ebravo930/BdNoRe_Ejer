from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Conexión a MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"  # O conexión a MongoDB Atlas
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.test_database
collection = database.items  # Cambiar si quieren otro nombre de colección

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de MongoDB con FastAPI"}

@app.get("/items/")
async def get_items():
    items = []
    async for item in collection.find():
        items.append(item)
    return items


@app.post("/items/")
async def create_item(item: dict):
    new_item = await collection.insert_one(item)
    created_item = await collection.find_one({"_id": new_item.inserted_id})
    return created_item
