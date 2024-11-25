import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo.errors import PyMongoError

from backend.config import settings
from backend.routers import (
    license_detection,
    vehicles,
    hotspots,
    users,
    auth,
    routes,
    websocket,
    reservations,
    statistics,
)
from fastapi import HTTPException, Depends
from backend.utils.auth_scheme import auth_scheme
from backend.utils.auth import role_required
from backend.models.user import RoleEnum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def init_app():
    print('init')


app.add_event_handler('startup', init_app)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={'detail': exc.errors(), 'message': 'Validation error'},
    )


@app.exception_handler(PyMongoError)
async def mongo_transaction_exception_handler(request: Request, exc: PyMongoError):
    if hasattr(request.state, 'session') and request.state.session:
        try:
            await request.state.session.abort_transaction()
        except Exception as abort_exc:
            print(f'Failed to abort transaction: {abort_exc}')

    return JSONResponse(
        status_code=500,
        content={
            'message': 'A MongoDB error occurred. The transaction has been aborted.'
        },
    )


app.include_router(auth.router, tags=['auth'], prefix='/auth')

app.include_router(
    users.router,
    tags=['users'],
    prefix='/users',
    dependencies=[Depends(auth_scheme)],
)

app.include_router(
    statistics.router,
    tags=['statistics'],
    prefix='/statistics',
    dependencies=[Depends(auth_scheme)],
)

app.include_router(
    license_detection.router,
    tags=['license-detection'],
    prefix='/license-detection',
    dependencies=[Depends(auth_scheme)],
)


app.include_router(
    vehicles.router,
    tags=['vehicles'],
    prefix='/vehicles',
    dependencies=[Depends(auth_scheme)],
)

app.include_router(
    routes.router,
    tags=['routes'],
    prefix='/routes',
    dependencies=[Depends(auth_scheme)],
)

app.include_router(
    hotspots.router,
    tags=['hotspots'],
    prefix='/hotspots',
    dependencies=[Depends(auth_scheme)],
)

app.include_router(
    reservations.router,
    tags=['reservations'],
    prefix='/reservations',
    dependencies=[Depends(auth_scheme)],
)


app.include_router(
    websocket.router,
    tags=['websocket'],
    prefix='/websocket',
)


def start():
    uvicorn.run(
        'backend.main:app',
        host='0.0.0.0',
        port=settings.port,
        reload=settings.debug,
        log_level='info',
    )


if __name__ == '__main__':
    start()
