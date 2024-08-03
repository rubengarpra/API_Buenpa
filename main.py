from fastapi import FastAPI
from routers import news

app = FastAPI()

#ROUTERS
app.include_router(news.router)

