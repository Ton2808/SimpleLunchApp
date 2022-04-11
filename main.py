from fastapi import FastAPI
from core.db.database import engine
from core.db import models
from routers import user, store
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(store.router)
app.include_router(user.router)
