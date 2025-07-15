#!/usr/bin/env bash

docker run --name datastar-events-demo \
  -v $(pwd):/app \
  -v /app/.venv \
  --net=host \
  --rm \
  datastar-events-demo 


