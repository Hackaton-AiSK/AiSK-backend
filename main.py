from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI()

# allow CORS
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(router)

if __name__ == "__main__":

    uvicorn.run("main:app", host="localhost", port=8000,reload=True)