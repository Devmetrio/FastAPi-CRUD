from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def helloworld():
    return "helloworld"