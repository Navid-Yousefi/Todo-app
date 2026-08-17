from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.router import router as users_routes
from users.model import UserModel
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield

    print("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(tasks_routes)
app.include_router(users_routes)

origins = [
    'http://127.0.0.1:5500'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.exception_handler(StarletteHTTPException)
async def http_excption_handler(request, exc):
    error_response = {
        'error': True,
        'status_code': exc.status_code,
        'detail': str(exc.detail)
    }
    return JSONResponse(status_code=exc.status_code, content=error_response)

@app.exception_handler(RequestValidationError)
async def http_validation_excption_handler(request, exc):
    error_response = {
        'error': True,
        'status_code': status.HTTP_422_UNPROCESSABLE_CONTENT,
        'detail': 'Ther was a problem with your request',
        'content': exc.errors()
    }
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=error_response)
