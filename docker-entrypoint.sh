#!/bin/sh

container_type=${CONTAINER_TYPE-FAST_API};

if [ "$container_type" = "FAST_API" ]; then
  uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
fi;
