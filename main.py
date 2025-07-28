from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
async def backend(request: Request):
    return templates.TemplateResponse("about/datastar.html", {"request": request})

@app.get("/about/events", response_class=HTMLResponse)
async def backend(request: Request):
    return templates.TemplateResponse("about/events.html", {"request": request})

@app.get("/about/uswds", response_class=HTMLResponse)
async def backend(request: Request):
    return templates.TemplateResponse("about/uswds.html", {"request": request})
