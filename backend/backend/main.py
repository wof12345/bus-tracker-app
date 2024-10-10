from backend.routers import license_detection
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import PendingRollbackError

from backend.config import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def init_app():
    print('int')


app.add_event_handler('startup', init_app)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={'detail': exc.errors(), 'message': 'Validation error'},
    )


@app.exception_handler(PendingRollbackError)
async def pending_rollback_exception_handler(
    request: Request, exc: PendingRollbackError
):
    if hasattr(request.state, 'db'):
        request.state.db.rollback()

    return JSONResponse(
        status_code=500,
        content={
            'message': 'A database error occurred. The transaction has been rolled back.'
        },
    )


app.include_router(
    license_detection.router, tags=['license-detection'], prefix='/license-detection'
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
