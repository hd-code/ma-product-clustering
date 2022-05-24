cd $(dirname $0)
docker rmi -f pandoc-skill
docker build -t pandoc-skill .
