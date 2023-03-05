from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from core.routers import carbrand_routers, carmodel_routers

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(carbrand_routers.router, tags=['Car Brand'], prefix='/api/brands')
app.include_router(carmodel_routers.router, tags=['Car Model'], prefix='/api/models')


@app.get('/api/car')
def root():
    return {'message': 'Hello World'}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)


