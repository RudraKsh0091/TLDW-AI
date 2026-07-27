print("1. main.py started", flush=True)

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
print("2. FastAPI imported", flush=True)

from app.api.routes import router
print("3. routes imported", flush=True)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TLDW AI",
    version="1.0.0",
)
print("4. app created", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome://extensions/?id=ancbldnggpncgibggpgcahoamlkllmmc",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
print("5. router included", flush=True)