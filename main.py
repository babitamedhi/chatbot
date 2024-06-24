from fastapi import FastAPI
from Scripts.start import router as start_router
from Scripts.reply import router as reply_router

app = FastAPI()

app.include_router(start_router)
app.include_router(reply_router)

if __name__ == "__main__":
    print("Starting Uvicorn")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
