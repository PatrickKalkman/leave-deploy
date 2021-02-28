#!/bin/bash
VERSION="0.8.1"
ARCH="x86_64"
APP="cassava-model-service"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
docker build -f $DIR/Dockerfile -t $ARCH/$APP:$VERSION .
