from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import input_detection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class data_input(BaseModel):
    data: str

@app.post("/text-analyze/api", response_class=HTMLResponse)
async def analyze_input(data_input: Request):
    data = await data_input.body()
    input_data = data.decode()
    print(input_data)
    input_detection.input_detection(input_data)

    with open("output.txt", "r", encoding="utf-8") as file:
        lines_from_file = file.readlines()

    analyzed_data = '<br>'.join(lines_from_file)
    #str(analyzed_data)
    #print(analyzed_data)
    html = f'<p>{analyzed_data}</p>'

    return html