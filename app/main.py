import os

from fastapi import FastAPI

app = FastAPI(title="LangChain HITL")

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "LangChain Human-in-the-Loop API"}
