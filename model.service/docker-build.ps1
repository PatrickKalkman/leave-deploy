$VERSION="0.8.1"
$ARCH="x86_64"
$APP="cassava-model-service"
docker build -f ./Dockerfile -t ${ARCH}/${APP}:${VERSION} .
