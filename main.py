from fastapi import FastAPI
from endpoints.api import router as api_v1_router
from contextlib import asynccontextmanager
from db.session import engine, Base



@asynccontextmanager
async def lifespan(app : FastAPI):
    # start up events
    Base.metadata.create_all(bind=engine)
    yield
    

app = FastAPI(lifespan=lifespan)


@app.get("/health_check")
async def test_endpoint():
    return {
        "detail" : "ok"
    }
    
    
app.include_router(api_v1_router, prefix="/api/v1")