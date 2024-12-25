from fastapi import FastAPI
from routes.identities import identities_router


app = FastAPI()

version_prefix = "v1"


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(identities_router, prefix=f"/api/{version_prefix}")
