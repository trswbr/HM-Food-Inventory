# import packages
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


# import code
from FI_API.internal.config import api_host, api_port
from FI_API.internal.hmdb import connect_database, close_database
from FI_API.endpoints.api import api_router


## main app ## -------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    yield
    close_database()


app = FastAPI(
    lifespan=lifespan,
    title="Home Manager - Lebensmittelverwaltung",
    description="API für die Lebensmittelverwaltungsanwendung im Home Manager Projekt",
    version="1.0.0",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router) # alt prefix ergänzen für verschiedene versionen

def get_app():
    """
    Import of FastAPI app for testing.
    bash for test start: pytest -q
    """
    return app

if __name__ == "__main__":
    uvicorn.run("FI_API.main:app", host=api_host, port=int(api_port), reload=True)

## start: python -m FI_API.main
