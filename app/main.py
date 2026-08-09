from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.router import router as users_routes
from users.model import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Application startup')
    yield

    print('Application shutdown')


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_routes)
app.include_router(users_routes)

# from auth.token_auth import get_authenticated_user

# @app.get('/public')
# def public_route():
#     return {'message': 'This is a public route.'}


# @app.get('/private')
# def private_route(user = Depends(get_authenticated_user)):
#     print(user)
#     return {'message': 'This is a private route.'}