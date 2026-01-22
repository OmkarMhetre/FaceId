from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth_routes import router as auth_router
from backend.routes.face_routes import router as face_router
from backend.routes.recognize import router as recognize_router
from backend.routes.recognize import router as attendance_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(face_router)
app.include_router(face_router)
app.include_router(recognize_router)
app.include_router(attendance_router)

@app.get("/")
def home():
    return {"message": "Backend running"}
