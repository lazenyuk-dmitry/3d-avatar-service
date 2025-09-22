from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os
import uuid
from mesh_generator import generate_avatar

app = FastAPI(title="3D Avatar Service")

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "3D Avatar API is running"}


@app.post("/generate-avatar/")
async def generate_avatar_endpoint(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    output_path = os.path.join(UPLOAD_DIR, f"avatar_{uuid.uuid4()}.glb")

    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())

        generate_avatar(input_path, output_path)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    file_url = f"/download/{os.path.basename(output_path)}"
    return JSONResponse(content={"status": "success", "model_url": file_url})


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="model/gltf-binary", filename=filename)
