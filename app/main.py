from fastapi import FastAPI, status
from app.user.router import router as user_router


app = FastAPI(
    title="Authentication Server API"
)

@app.get("/ready", status_code=status.HTTP_200_OK)
def is_ready():
    return {"Description": "OK"}

app.include_router(user_router)
