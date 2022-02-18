DIR="pim"

if [ ! -d "$(dirname $0)/$DIR" ]
then
  echo "Akeneo project does not exist. Creating project ..."
  cd "$(dirname $0)"
  docker run -it --rm -u www-data -v $(pwd)/$DIR:/srv/pim -w /srv/pim akeneo/pim-php-dev:5.0 \
    php -d memory_limit=4G /usr/local/bin/composer create-project --prefer-dist \
    akeneo/pim-community-standard /srv/pim "5.0.*@stable"
  exit 0
fi

cd "$(dirname $0)/$DIR"

# ------------------------------------------------------------------------------

start_queue() {
  echo "Starting job queue"
  docker-compose run -d --rm -u www-data --name akeneo_job_queue php \
    php bin/console akeneo:batch:job-queue-consumer-daemon
}
stop_queue() {
  echo "Stopping job queue"
  docker stop akeneo_job_queue
}

# ------------------------------------------------------------------------------

CMD=$1
shift

case $CMD in
  up)
    make up
    start_queue
    ;;
  down)
    stop_queue
    make down
    ;;

  init)
    make prod
    start_queue
    echo "--- Create first user to be able to login"
    docker-compose run --rm -u www-data php php bin/console pim:user:create
    ;;
  init-dev)
    make dev
    start_queue
    ;;

  refresh)
    rm -rf vendor node_modules
    make vendor
    make upgrade-front
    ;;
  update)
    rm -rf vendor node_modules
    rm composer.lock yarn.lock
    make vendor
    make upgrade-front
    ;;

  run)
    case $1 in
      node|yarn)
        docker-compose run --rm -u node "$@"
        ;;
      *)
        docker-compose run --rm -u www-data php "$@"
        ;;
    esac
    ;;

  *)
    echo "Usage: $0 TASK"
    echo "  up       - starts Akeneo PIM"
    echo "  down     - stops Akeneo PIM"
    echo ""
    echo "  init     - (re)creates blank Akeneo PIM for production"
    echo "  init-dev - (re)creates Akeneo PIM in dev mode with some sample data"
    echo ""
    echo "  refresh  – refreshes the installation e.g. after dependency updates"
    echo "  update   – updates all dependencies to their latest version and refreshes the installation"
    echo ""
    echo "  run CMD  - runs a command like 'php ...' or 'yarn ...' inside Akeneo PIM"
    ;;
esac
