from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from api.user_router import user_router
from api.profile_router import profile_router

from persistence.tables import metadata_obj

os.makedirs("media/avatars", exist_ok=True)

app = FastAPI(title="PokeAPI", openapi_prefix="/api")

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(user_router)
app.include_router(profile_router)


if __name__ == "__main__":
    import uvicorn
    print('Starting FastAPI...')
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)