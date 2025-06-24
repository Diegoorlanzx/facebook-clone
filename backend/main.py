from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Facebook Clone API is running"}
