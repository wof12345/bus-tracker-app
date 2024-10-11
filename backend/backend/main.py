import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo.errors import PyMongoError

from backend.config import settings
from backend.routers import license_detection, vehicles

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


app.include_router(
    license_detection.router, tags=['license-detection'], prefix='/license-detection'
)


app.include_router(vehicles.router, tags=['vehicles'], prefix='/vehicles')


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
