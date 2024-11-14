from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome...to gAIn!"}

@app.get("/square_root/")
async def square_root(x: float = 1, y: float = 2):
    z = x**2 + y**2
    return z**0.5