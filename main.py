from fastapi import FastAPI
from routers import news, events

app = FastAPI()

#ROUTERS
app.include_router(news.router)
app.include_router(events.router)

