from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.dni import dni_router
from routes.ruc import ruc_router


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        # "https://codemaster.com.pe",
        # "https://www.codemaster.com.pe",
        # "https://std-pichari.codemaster.com.pe",
        # "http://localhost:3000",
    ],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

version_v1_prefix = "v1"


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(dni_router, prefix=f"/api/{version_v1_prefix}")
app.include_router(ruc_router, prefix=f"/api/{version_v1_prefix}")
