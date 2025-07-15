#!/usr/bin/env bash

docker run --name datastar-events-demo \
  --net=host \
  --rm \
  datastar-events-demo 


  # -v $(pwd)/jinja:/app/jinja \
