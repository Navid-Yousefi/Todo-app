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



from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import httpx
from core.config import settings


redis = aioredis.from_url(settings.REDIS_URL)
cache_backend = RedisBackend(redis)
FastAPICache.init(cache_backend, prefix='fastapi-cache')


async def request_current_weather(latitude: float, longitude: float):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,relative_humidity_2m'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_weather = data.get('current', {})
        return current_weather
    else:
        return None

@app.get('/fetch-current-weather', status_code=status.HTTP_200_OK)
@cache(expire=20)
async def fetch_current_weather(latitude: float = 40.7128, longitude: float = -74.0060):
    current_weather = await request_current_weather(latitude, longitude)
    if current_weather:
        return JSONResponse(content={'current_weather': current_weather})
    else:
        return JSONResponse(content={'detail': 'Failed to fetch weather'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



from core.email_util import send_email

@app.get('/test-send-mail', status_code=status.HTTP_200_OK)
async def test_send_mail():
    await send_email(
        subject='Test Email from Fastapi',
        recipients=['naviddeveloper2002@gmail.com'],
        body='This is a test email sent using the email_util function'
    )
    return JSONResponse(content={'detail': 'Email has been sent'})
