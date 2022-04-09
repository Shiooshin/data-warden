from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from os import path

import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    filename = path.abspath(path.join(path.dirname(__file__), 'static/index.html'))

    with open(filename, 'r') as html_content:
        return HTMLResponse(content=html_content.read(), status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
