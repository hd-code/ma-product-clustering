cd $(dirname $0)
SELF="./$(basename $0)"

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

    *)
        echo "Usage: $0 CMD"
        echo "  start     – restart pim"
        echo "  stop      – stop pim"
        echo "  run       – run a command like 'php ...' in akeneo pim"
        echo "  setup     – creates new akeneo instance"
        echo "  setup-dev – like setup but with test data"
        echo "  teardown  – destroy akeneo instance for good"
        ;;
esac
