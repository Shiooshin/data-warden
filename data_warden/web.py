from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import uvicorn

app = FastAPI()


@app.get("/")
async def root():

    with open('static/starter.html', 'r') as html_content:
        return HTMLResponse(content=html_content.read(), status_code=200)


@app.get("/dash")
async def dash():

    with open('static/index.html', 'r') as html_content:
        return HTMLResponse(content=html_content.read(), status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
