import logging
import uuid
from functools import lru_cache

from fastapi import FastAPI, Request

from app.configs.environment import get_environment_variables
from app.database.base_model import init
from app.routers.post_router import PostRouter

# Application Environment Configuration
env = get_environment_variables()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Output logs to the console
)


def update_examples():
    # Generate new example values
    app.openapi_schema["components"]["schemas"]["PostSchema-Input"]["properties"]["id"][
        "examples"
    ] = [str(uuid.uuid4()) for _ in range(10)]


app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
)

# Add Routers
app.include_router(PostRouter)


@app.on_event("startup")
def on_startup():
    if app.openapi_schema:
        update_examples()


# Use the custom event handler as a dependency for your routes
@app.middleware("http")
async def custom_event_middleware(request: Request, call_next):
    if request.url.path.startswith("/docs"):
        # This code runs when the Swagger documentation is accessed
        if app.openapi_schema:
            update_examples()
    response = await call_next(request)
    return response


# Initialise Data Model Attributes
init()
