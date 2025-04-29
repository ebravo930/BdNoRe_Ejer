from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Conexión a MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"  
client = AsyncIOMotorClient(MONGO_DETAILS, serverSelectionTimeoutMS=5000)  # Timeout de conexión
database = client.test_database
collection = database.items  

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

@app.get("/pingdb/")
async def ping_database():
    try:
        # Intentar hacer ping a la base de datos
        await client.admin.command('ping')
        return {"message": "Conexión a MongoDB exitosa"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo conectar a MongoDB: {str(e)}")
