from fastapi import FastAPI, Request, Depends
from api.common.logger import logger

from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.routers import user_router, project_router
from api.data.database import on_startup
from api.common.security import verify_api_key
from api.common.settings import settings

limiter = Limiter(
    key_func=lambda request: request.client.host,
    default_limits=["5/minute"]
)

app = FastAPI(
    title="FastAPI JWT & RBAC",
    description="This is a FastAPI project with JWT authentication and Role-Based Access Control.",
    version="1.0.0",
    on_startup=[on_startup],
    dependencies=[Depends(verify_api_key)]
)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    logger.warning("Rate limit exceeded for request: %s", request.url)
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

logger.info("Application started with title: %s", app.title)


app.include_router(user_router.router,prefix="/api/auth", tags=["Authentication"])
app.include_router(project_router.router, prefix="/api/projects", tags=["Projects"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Projects API",
        version="1.0.0",
        description="This is a FastAPI project with JWT authentication and Role-Based Access Control.",
        summary= "",
        tags="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
