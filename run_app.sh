

docker build -t reliable_api . --network="host"
docker run -p 5008:5008 reliable_api
