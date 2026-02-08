from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from mock_data import create_mock_data
from routes.api import get_requests_store, router

app = FastAPI(title="LangChain HITL")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(router)

# Get requests store and initialize mock data on startup
requests_store = get_requests_store()
create_mock_data(requests_store)
