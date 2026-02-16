from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.events import router as events_router
from app.routes.bookings import router as bookings_router
 #

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    print("Database Connected successfully")
    yield
    print("Database disconnected .....")



app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, tags=["Authentication"])
app.include_router(events_router, tags=["Events"])
app.include_router(bookings_router, tags=["Bookings"])
@app.get("/")
async def test_root():
    return {"mesage":"Hello Suckers!"}