from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Choose Your Own Adventure API",
    description="An API to generate adventure stories using OpenAI.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home(request: Request):
    """Serve the main HTML interface."""
    return {"message": "Hello from the backend!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
