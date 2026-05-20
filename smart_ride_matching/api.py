from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth import login, signup

app = FastAPI(title="Smart Ride Matching API")

# Configure CORS to allow the React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def api_login(request: AuthRequest):
    success, message = login(request.username, request.password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    return {"success": True, "message": message}

@app.post("/api/signup")
def api_signup(request: AuthRequest):
    success, message = signup(request.username, request.password)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}

@app.get("/")
def read_root():
    return {"message": "Smart Ride API is running"}
