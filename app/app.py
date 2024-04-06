import os
from contextlib import asynccontextmanager

from di import DI, DIContainer
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Engine, create_engine
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from application import UnitOfWork
from domain.model.user import UserRepository, EncryptionService
from exception import SystemException
from port.adapter.persistence.repository.inmem import InMemUserRepository, InMemUnitOfWork
from port.adapter.persistence.repository.mysql import DataBase, MySQLUnitOfWork
from port.adapter.resource.auth import auth_resource
from port.adapter.resource.health import health_resource
from port.adapter.resource.user import user_resource
from port.adapter.service.user import EncryptionServiceImpl


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    DI_LIST = [
        DI.of(UnitOfWork, {'MySQL': MySQLUnitOfWork}, InMemUnitOfWork),
        DI.of(UserRepository, {}, InMemUserRepository),
        DI.of(EncryptionService, {}, EncryptionServiceImpl),
    ]

    if 'MySQL' in os.getenv('DI_PROFILE_ACTIVES'):
        engine: Engine = create_engine(
            'mysql://{username}:{password}@{host}:{port}/{database}?{options}'.format(
                username=os.getenv('DATABASE_USERNAME'),
                password=os.getenv('DATABASE_PASSWORD'),
                host=os.getenv('DATABASE_HOST'),
                port=3306,
                database=os.getenv('DATABASE'),
                options='charset=utf8mb4' if os.getenv('MODE') == 'local' else 'ssl_mode=VERIFY_IDENTITY&charset=utf8mb4'
            ),
            echo=os.getenv('LOG_LEVEL', 'DEBUG') == 'DEBUG'
        )
        DI_LIST.append(DI.of(Engine, {}, engine))
        DataBase.metadata.create_all(bind=engine)

    [DIContainer.instance().register(di) for di in DI_LIST]
    yield
    # 終了後

app = FastAPI(title='Identity Access', root_path=os.getenv('OPENAPI_PREFIX'), lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_resource.router)
app.include_router(health_resource.router)
app.include_router(user_resource.router)


@app.exception_handler(SystemException)
async def system_exception_handler(request: Request, exception: SystemException):
    exception.logging()
    return JSONResponse(
        status_code=exception.error_code.http_status,
        content=jsonable_encoder({
            "type": exception.error_code.name,
            "title": exception.error_code.message,
            "status": exception.error_code.http_status,
            "instance": str(request.url)
        }),
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, error: ValueError):
    print(error)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({
            "type": "CLIENT_2001",
            "title": "不正なリクエストです",
            "status": 400,
            "instance": str(request.url)
        }),
    )


@app.exception_handler(AssertionError)
async def assertion_error_handler(request: Request, error: AssertionError):
    print(error)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({
            "type": "CLIENT_2002",
            "title": "不正なリクエストです",
            "status": 400,
            "instance": str(request.url)
        }),
    )
