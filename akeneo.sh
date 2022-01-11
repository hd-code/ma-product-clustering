DIR="akeneo-pim"

if [ ! -d "$(dirname $0)/$DIR" ]
then
    cd "$(dirname $0)"
    docker run -it --rm -u www-data -v $(pwd)/$DIR:/srv/pim -w /srv/pim akeneo/pim-php-dev:5.0 \
        php -d memory_limit=4G /usr/local/bin/composer create-project --prefer-dist \
        akeneo/pim-community-standard /srv/pim "5.0.*@stable"
    exit 0
fi

cd "$(dirname $0)/$DIR"
SELF="../$(basename $0)"

CMD=$1
shift

case $CMD in
    run)
        export APP_ENV=dev
        docker-compose run --rm php "$@"
        ;;

    start)
        docker-compose start
        $SELF start_queue
        ;;
    stop)
        $SELF stop_queue
        docker-compose stop
        ;;

    setup)
        make prod
        $SELF run php bin/console pim:user:create
        $SELF start_queue
        ;;
    setup-dev)
        make dev
        $SELF start_queue
        ;;
    teardown)
        $SELF stop_queue
        make down
        ;;


    start_queue)
        echo "Starting job queue..."
        export APP_ENV=dev
        docker-compose run -d --rm --name akeneo_job_queue php \
            php bin/console akeneo:batch:job-queue-consumer-daemon
        ;;
    stop_queue)
        echo "Stopping job queue..."
        docker stop akeneo_job_queue
        docker rm -v akeneo_job_queue
        ;;

    install_icecat)
        alias docker_php='docker-compose run -u www-data --rm php php'
        alias docker_yarn='docker-compose run -u node --rm node yarn'
        docker_php bin/console cache:clear --env=prod
        docker_php bin/console pim:installer:assets --symlink --clean --env=prod
        docker_php bin/console d:s:u --force
        docker_yarn run webpack
        docker_yarn run update-extensions
        docker_yarn run less
        ;;

    *)
        echo "Usage: $0 CMD"
        echo "  run       – run a command like 'php ...' in akeneo pim"
        echo "  start     – restart pim"
        echo "  stop      – stop pim"
        echo "  setup     – creates new akeneo instance"
        echo "  setup-dev – like setup but with test data"
        echo "  teardown  – destroy akeneo instance for good"
        ;;
esac
