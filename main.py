# /// script
# dependencies = [
#   "datastar-py",
#   "fastapi",
#   "uvicorn",
# ]
# [tool.uv.sources]
# datastar-py = { path = "../../" }
# ///

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from datetime import datetime

from fastapi.responses import HTMLResponse, StreamingResponse

from datastar_py.fastapi import (
    DatastarResponse,
    ReadSignals,
    ServerSentEventGenerator,
)


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about/backend", response_class=HTMLResponse)
async def backend(request: Request):
    return templates.TemplateResponse("about/backend.html", {"request": request})


@app.get("/about/datastar", response_class=HTMLResponse)
async def datastar(request: Request):
    return templates.TemplateResponse("about/datastar.html", {"request": request})


@app.get("/about/events", response_class=HTMLResponse)
async def events(request: Request):
    return templates.TemplateResponse("about/events.html", {"request": request})


@app.get("/about/uswds", response_class=HTMLResponse)
async def uswds(request: Request):
    return templates.TemplateResponse("about/uswds.html", {"request": request})


@app.get("/demos/story-time", response_class=HTMLResponse)
async def story_time(request: Request):
    return templates.TemplateResponse("demos/story-time.html", {"request": request})


async def build_book_contents(snippet):
    current_text = ""

    for word in snippet:
        current_text += f" {word}"
        yield ServerSentEventGenerator.patch_elements(
            f"<section id='book-contents'>{current_text}</section>"
        )
        await asyncio.sleep(0.1)


@app.get("/demos/story-time/read/{book_title}", response_class=StreamingResponse)
async def read_book(request: Request, signals: ReadSignals):
    print("signals: ", signals)
    book_title = request.path_params["book_title"]
    # Open the file in read mode
    file = open(f"./static/books/{book_title}.txt", "r")

    # Read the entire content of the file
    content = file.read()
    # FIXME :: need to start the content after the following marker:
    # start_of_book = content  # *** START OF THE PROJECT GUTENBERG EBOOK
    #
    # Also need to ensure \n characters are used to assemble <p> tags
    #
    # Also need to have a way for the client to pause or cancel the stream
    #
    # Close the file
    file.close()
    snippet = content.split(" ")

    return DatastarResponse(build_book_contents(snippet))
