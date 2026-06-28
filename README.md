# Datastar <--> FastAPI

This project uses FastAPI and Datastar to demonstrate a lighter, leaner approach to creating responsive and reactive web application.
The Python environment is housed entirely in a docker container, so you should only need docker installed on your machine to run this.

Further details about the project and how it works can be found either by reviewing the code or navigating the application once running.

## Getting Started

1. Run `./build.sh` to build and tag the docker container housing the Python environment for local use.
2. Run `./start.sh` to start the server up.

FastAPI is set to hot-reload changes to files in the mounted volume, so you shouldn't need to start and stop the backend once it's running. Automatic reloading of the client page in the browser is not yet set up.

Go to <http://localhost:8000> to view the home page. The site will give you instructions from there.

NOTE :: If you are running this on MacOS (and perhaps Windows, still need to test), you may need to click the "Enable host networking" in your Docker Desktop settings before the page will load. Linux environments shouldn't need any adjustment.
