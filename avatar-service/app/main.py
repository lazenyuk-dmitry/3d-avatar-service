from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid

from mesh_generator import generate_avatar

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="3D Avatar Service")


app.mount("/files", StaticFiles(directory=str(UPLOAD_DIR)), name="files")


@app.get("/")
def root():
    return {"message": "3D Avatar API is running"}


@app.post("/generate-avatar/")
async def generate_avatar_endpoint(request: Request, file: UploadFile = File(...)):
    input_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"

    output_name = f"avatar_{uuid.uuid4()}.glb"
    output_path = UPLOAD_DIR / output_name

    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        print(f"[API] Input -> {input_path}")
        print(f"[API] Output target -> {output_path}")
        generate_avatar(str(input_path), str(output_path))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

    if not output_path.exists():
        raise HTTPException(status_code=500, detail=f"Generated file not found: {output_path}")

    file_url = f"{request.base_url}files/{output_name}"

    return JSONResponse({"status": "ok", "model_url": file_url})
