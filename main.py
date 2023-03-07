from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from core.routers import carbrands_routers, carmodels_routers

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


app.include_router(carbrands_routers.router, tags=['Car'], prefix='/api/carbrands')
app.include_router(carmodels_routers.router, tags=['Car'], prefix='/api/carmodels')


@app.get('/api')
def root():
    return {'message': 'Hello World'}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)


