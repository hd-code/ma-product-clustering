DIR="pim"

if [ ! -d "$(dirname $0)/$DIR" ]
then
  DIR_TMP=$(pwd)
  cd "$(dirname $0)"
  docker run -it --rm -u www-data -v $(pwd)/$DIR:/srv/pim -w /srv/pim akeneo/pim-php-dev:5.0 \
    php -d memory_limit=4G /usr/local/bin/composer create-project --prefer-dist \
    akeneo/pim-community-standard /srv/pim "5.0.*@stable"
  cd "$DIR_TMP"
fi

cd "$(dirname $0)/$DIR"

run_in_php() { docker-compose run --rm -u www-data php "$@"; }
run_in_node() { docker-compose run --rm -u node node "$@"; }

start_queue() {
  echo "Starting job queue"
  docker-compose run -d --rm -u www-data --name akeneo_job_queue php \
    php bin/console akeneo:batch:job-queue-consumer-daemon
}
stop_queue() {
  echo "Stopping job queue"
  docker stop akeneo_job_queue
  docker rm -v akeneo_job_queue
}

CMD=$1
shift

case $CMD in
  run)
    run_in_php "$@"
    ;;
  run_node)
    run_in_node "$@"
    ;;

  start)
    docker-compose start
    start_queue
    ;;
  stop)
    stop_queue
    docker-compose stop
    ;;

  setup)
    make prod
    echo "--- Create first user to be able to login"
    run_in_php php bin/console pim:user:create
    start_queue
    ;;
  setup-dev)
    make dev
    start_queue
    ;;
  teardown)
    stop_queue
    docker-compose stop
    make down
    ;;

  *)
    echo "Usage: $0 CMD"
    echo "  run       – run a command like 'php ...' in akeneo pim"
    echo "  run_node  – run a command like 'yarn ...' in akeneo pim"
    echo "  start     – restart pim"
    echo "  stop      – stop pim"
    echo "  setup     – creates new akeneo instance"
    echo "  setup-dev – like setup but with test data"
    echo "  teardown  – destroy akeneo instance for good"
    ;;
esac
