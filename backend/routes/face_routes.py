from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import face_recognition
import numpy as np
import io
from PIL import Image

from backend.db.mysql_utils import add_face_to_db, get_all_faces

router = APIRouter()


@router.post("/add-face")
async def add_face(
    name: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")

        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(pil_image)

        encodings = face_recognition.face_encodings(image_np)

        if len(encodings) == 0:
            raise HTTPException(status_code=400, detail="No face detected")

        if len(encodings) > 1:
            raise HTTPException(status_code=400, detail="Multiple faces detected")

        encoding = encodings[0]  # numpy array (128,)
        encoding_bytes = encoding.tobytes()

        add_face_to_db(name, encoding_bytes)

        return {
            "message": "Face encoding stored successfully",
            "name": name
        }

    except HTTPException:
        raise

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.get("/list-faces")
async def list_faces():
    try:
        faces = get_all_faces()

        result = []
        for name, encoding_bytes in faces:
            encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
            result.append({
                "name": name,
                "encoding": encoding.tolist()
            })

        return {
            "count": len(result),
            "faces": result
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
