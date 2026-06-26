# Datastar <--> uv

1. Run `./build.sh` to build and tag the docker container housing the Python environment for local use.
2. Run `./start.sh` to start the server up.

FastAPI is set to hot-reload changes to files in the mounted volume, so you shouldn't need to do any fiddling once it's running.

Go to <http://localhost:8000> to view the home page. The site will give you instructions from there.

NOTE :: If you are running this on MacOS (and perhaps Windows, still need to test), you may need to click the "Enable host networking" in your Docker Desktop settings before the page will load.
