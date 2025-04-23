from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.segmentation_service import router as segmentation_router

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the API route
app.include_router(segmentation_router, prefix="/api")

app.mount("/static", StaticFiles(directory="data/outputs"), name="static")

@app.get("/")
def root():
    return {"message": "Breast Tumor Segmentation Backend is Running"}
