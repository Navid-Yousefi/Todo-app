from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes



@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Application startup')
    yield

    print('Application shutdown')


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_routes, prefix='/todo')