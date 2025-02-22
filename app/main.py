from fastapi import FastAPI
from app.api.endpoints import auth, users
import logging
import sys

app = FastAPI(title="FastAPI JWT Auth")

app.include_router(auth.router, tags=["authentication"], prefix="/auth")
app.include_router(users.router, tags=["users"], prefix="/users")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)