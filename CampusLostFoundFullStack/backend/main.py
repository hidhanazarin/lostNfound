from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
from datetime import datetime
from typing import List, Optional
import os

app = FastAPI()

# ==============================
# In-memory database (temporary)
# ==============================
items_db: List[dict] = []

# ==============================
# CORS Configuration
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Static Files Setup
# frontend is sibling of backend
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Mount static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Serve index.html at root
@app.get("/")
async def serve_home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ==============================
# API Endpoints
# ==============================

# Add item
@app.post("/add-item")
async def add_item(
    type: str = Form(...),
    title: str = Form(...),
    location: str = Form(...),
    contact: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None)
):
    image_url = None

    if image:
        file_id = str(uuid.uuid4())
        image_url = f"/fake-images/{file_id}_{image.filename}"

    item = {
        "id": str(uuid.uuid4()),
        "type": type,
        "title": title,
        "location": location,
        "contact": contact,
        "description": description,
        "category": category,
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }

    items_db.append(item)

    return {
        "message": "Item added successfully",
        "item": item
    }


# Get items (optional filter by type)
@app.get("/items")
def get_items(item_type: Optional[str] = Query(None)):
    filtered_items = items_db

    if item_type:
        filtered_items = [
            item for item in items_db
            if item["type"].lower() == item_type.lower()
        ]

    sorted_items = sorted(
        filtered_items,
        key=lambda x: x["created_at"],
        reverse=True
    )

    return sorted_items


# Delete item
@app.delete("/delete-item/{item_id}")
def delete_item(item_id: str):
    global items_db
    items_db = [
        item for item in items_db
        if item["id"] != item_id
    ]

    return {"message": "Item deleted successfully"}


# ==============================
# Local Development Run
# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
