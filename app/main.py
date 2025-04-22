from fastapi import FastAPI

from app import models, db
from app.routes.api_router import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api", tags=["api"])

models.Base.metadata.create_all(bind=db.engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
