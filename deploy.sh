#!/usr/bin/env bash

IMAGE=registry.cutt.com/p/jparser

docker pull $IMAGE
docker rm -f jparser
docker run -d \
    -p 8838:8838 \
    --name jparser \
    $IMAGE

