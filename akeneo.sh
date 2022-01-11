DIR_BASE=$(dirname $0)
DIR_PIM=$DIR_BASE/akeneo-pim

JOB_CONTAINER=akeneo_job_queue

run_in_pim() {
    cd $DIR_PIM
    "$@"
    cd ..
}

run_in_php() {
    cd $DIR_PIM
    export APP_ENV=dev
    docker-compose run --rm php "$@"
    cd ..
}

# ------------------------------------------------------------------------------

CMD=$1
shift

case $CMD in
    run)
        run_in_php "$@"
        ;;

    start)
        run_in_pim docker-compose start
        $0 start_jobqueue
        ;;
    stop)
        $0 stop_jobqueue
        run_in_pim docker-compose stop
        ;;

    start_jobqueue)
        echo "Starting job queue..."
        export APP_ENV=dev 
        run_in_pim docker-compose run -d --rm --name $JOB_CONTAINER php \
            php bin/console akeneo:batch:job-queue-consumer-daemon
        ;;
    stop_jobqueue)
        echo "Stopping job queue..."
        docker stop $JOB_CONTAINER
        docker rm -v $JOB_CONTAINER
        ;;

    setup)
        run_in_pim make prod
        run_in_php php bin/console pim:user:create
        $0 start_jobqueue
        ;;
    setup-dev)
        run_in_pim make dev
        $0 start_jobqueue
        ;;
    teardown)
        $0 stop_jobqueue
        run_in_pim make down
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
