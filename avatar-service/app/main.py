from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from .mesh_generator import generate_avatar
import os
import uuid

app = FastAPI(title="3D Avatar Service")

@app.post("/generate-avatar/")
async def generate_avatar_endpoint(file: UploadFile = File(...)):
    temp_input = f"/tmp/{uuid.uuid4()}{file.filename}"
    output_path = f"/tmp/avatar{uuid.uuid4()}.glb"

    with open(temp_input, "wb") as f:
        f.write(await file.read())

    try:
        generate_avatar(temp_input, output_path)
    except Exception as e:
        return {"error": str(e)}

    return FileResponse(output_path, media_type="model/gltf-binary", filename="avatar.glb")

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "3D Avatar API is running"}
