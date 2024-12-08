from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from api.routers import llm_rag_chat, newsletter

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
    return {"message": "Welcome... to gAIn!"}


@app.get("/status")
async def get_api_status():
    return {
        "version": "1.0"
    }


# Serve the favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Additional routers here
app.include_router(llm_rag_chat.router, prefix="/llm-rag")
app.include_router(newsletter.router, prefix="/newsletters")


@app.on_event("startup")
async def print_routes():
    print("Available routes:")
    for route in app.routes:
        print(
            f"Path: {route.path} | Name: {route.name} | Methods: {route.methods}")
