from fastapi import FastAPI
from routes import register_routes

app = FastAPI()

register_routes(app)

@app.get("/")
def home():
    return {"message":"Welcome to the Core Banking System "}