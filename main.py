from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
app = FastAPI()

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://cris_bd:celustore123@cluster0.8yv65ix.mongodb.net/?retryWrites=true&w=majority")  # Cambia esto si tu MongoDB no está en localhost
db = client["cris_bd"]
collection = db["mi_coleccion"]


class DatosUsuario(BaseModel):
    usuario: str
    contra: str
    correcto: int
    pregunta: str
    pregunta_correcta: int


@app.post("/datos")
def agregar_datos(datos: DatosUsuario):
    documento = datos.dict()
    collection.insert_one(documento)
    return {"mensaje": "Datos agregados exitosamente"}


@app.get("/datos/{usuario}")
def obtener_datos(usuario: str):
    documento = collection.find_one({"usuario": usuario})
    if documento:
        documento["_id"] = str(documento["_id"])
        return documento
    return {"mensaje": "Usuario no encontrado"}


@app.put("/datos/{id}")
def actualizar_datos(usuario: str, datos: DatosUsuario):
    documento = collection.find_one({"usuario": usuario})
    _id = documento["_id"]
    campos_actualizar = datos.dict(exclude_unset=True)
    if campos_actualizar:
        resultado = collection.update_one({"_id": ObjectId(_id)}, {"$set": campos_actualizar})
        if resultado.modified_count == 1:
            return {"mensaje": "Datos actualizados exitosamente"}
    return {"mensaje": "Usuario no encontrado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)