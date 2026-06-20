# /// script
# dependencies = [
#   "datastar-py",
#   "fastapi",
#   "uvicorn",
# ]
# [tool.uv.sources]
# ///

import uuid
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

from datastar_py.consts import ElementPatchMode


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

connections: dict[str, dict] = {}


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


async def build_book_contents(snippet, word_offset: int, conn_id: str):
    """Stream words, checking per-connection pause/speed state."""
    current_text = ""

    for i, word in enumerate(snippet):
        if i < word_offset:
            continue

        # check pause state
        control = connections.get(conn_id)
        if control is None:
            break  # connection was cleaned up

        await control["pause_event"].wait()  # blocks when paused

        delay = 1.0 / control["wps"] if control["wps"] > 0 else 0.1

        current_text += f" {word}"
        yield ServerSentEventGenerator.patch_elements(
            f"<section id='book-contents'>{current_text}</section>"
        )
        await asyncio.sleep(delay)


@app.get("/demos/story-time/read/{book_title}", response_class=StreamingResponse)
async def read_book(request: Request, signals: ReadSignals):
    book_title = request.path_params["book_title"]
    word_offset = (signals or {}).get("offset", 0)

    # register per-connection state
    conn_id = str(uuid.uuid4())
    pause_event = asyncio.Event()
    pause_event.set()  # start unpaused
    connections[conn_id] = {
        "pause_event": pause_event,
        "wps": (signals or {}).get("wps", 5),
    }

    file = open(f"./static/books/{book_title}.txt", "r")

    # Read the entire content of the file
    content = file.read()
    # FIXME :: need to start the content after the following marker:
    # *** START OF THE PROJECT GUTENBERG EBOOK <name of book> ***
    # can probably just find that marker and set the word_offset to be that number + 1
    # Also need to ensure \n characters are used to assemble <p> tags
    # Close the file
    file.close()
    snippet = content.split(" ")

    # Build the response generator
    async def stream():
        # with the connection now established, tell the client what it's connection id is
        yield ServerSentEventGenerator.patch_signals(
            {"connId": conn_id, "offset": word_offset}
        )
        # then stream the book
        async for event in build_book_contents(snippet, word_offset, conn_id):
            yield event
        # cleanup on connection end
        connections.pop(conn_id, None)

    return DatastarResponse(stream())


@app.post("/demos/story-time/control", response_class=DatastarResponse)
async def control_stream(signals: ReadSignals):
    """Update per-connection stream attributes (pause, speed, etc.)."""
    conn_id = (signals or {}).get("connId")
    if not conn_id or conn_id not in connections:
        return DatastarResponse()  # 204 — no-op

    is_paused = False

    control = connections[conn_id]

    # if wps is currently set to 0, but a signal is setting it above 0, unpause
    if control["wps"] == 0 and signals["wps"] > 0:
        control["wps"] = signals["wps"]
        control["pause_event"].set()
    # if there is a pause signal, or the current wps is set above 0, but the
    # incoming signal sets it to zero, either action pauses the event stream
    elif signals["paused"] or (
        not signals["paused"] and signals["wps"] == 0 and control["wps"] > 0
    ):
        control["wps"] = signals["wps"]
        control["pause_event"].clear()
        is_paused = True
    else:
        control["wps"] = 1 if signals["wps"] == 0 else signals["wps"]
        control["pause_event"].set()

    async def update_client_signals():
        yield ServerSentEventGenerator.patch_signals(
            {"connId": conn_id, "paused": is_paused, "wps": control["wps"]}
        )

    return DatastarResponse(update_client_signals())  # 204
