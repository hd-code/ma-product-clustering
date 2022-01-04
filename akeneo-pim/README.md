# Akeneo PIM

## Installation & Setup

### Requirements

- docker 19+
- docker-compose 1.24+
- make

### Create User (Linux-only)

Akeneo needs to be run by a user with `uid=1000` and `gid=1000`.

So, Check the ids of your user account.

```sh
id
```

If you do not have the proper ids, follow these steps to create a user for running Akeneo-PIM:

1. Create group `akeneo` and user `akeneo`

```shell
sudo groupadd -g 1000 akeneo
sudo useradd akeneo -u 1000 -g 1000 -s /bin/bash
```

2. (optional) Disable password for user `akeneo`

```shell
sudo passwd -d akeneo
```

3. Add user `akeneo` to group `docker` to run docker containers with this user

```shell
sudo usermod -a -G docker akeneo
```

4. (optional) Add your user account to the group `akeneo` so you also have permissions for `pim` folder

```shell
sudo usermod -a -G akeneo $USER
```

5. Change ownership of the `pim` directory to make it editable for user `akeneo`

```shell
sudo chown -fR akeneo:akeneo $(pwd)/pim
```

### Installation and Setup

All following commands have to be executed as the correct user (see above) in the `pim` directory.

#### Dev

The dev environment comes with test data and advanced monitoring.

```shell
make dev
```

#### Prod

The prod environment contains no initial configuration whatsoever.

```shell
make prod
```

You have to manually create the first user in order to use Akeneo-PIM at all

```shell
APP_ENV=dev docker-compose run --rm php php bin/console pim:user:create
```

### Permissions of yarn Image

During the installation the following error may occur: `EACCES: permission denied, mkdir '/home/node/.yarn/v6'`

If that happens, the permissions for the yarn directory have to be changed. Just run:

```sh
docker-compose run -u root node chown -R node:node /home/node/.yarn
```

And retry the installation.

### Tearing down the Akeneo-PIM installation

The following command will stop the system, clear the installation and wipe all data. So, be careful!

```shell
make down
```

Afterwards a new instance can be created as described previously.

## Usage

Again, all following commands have to be executed as the correct user (see above) in the `pim` directory.

### Switch to the correct user (Linux-only)

```shell
su akeneo
```

### Starting and Stopping the Akeneo Services

After the `make` commands, the Akeneo services are all up and running already, so they don't have to be started again.

Stop the Akeneo cluster without deleting it:

```shell
docker-compose stop
```

Restart the Akeneo cluster:

```shell
docker-compose stop
```

### Job Queue

In order to run any Akeneo Jobs (like import or export), the job queue needs to be initialized. It should also be powered down before stopping the cluster.

Start the Job Queue:

```shell
APP_ENV=dev docker-compose run -d --rm --name akeneo_job_queue php \
    php bin/console akeneo:batch:job-queue-consumer-daemon
```

Stop and remove the Job Queue:

```shell
docker stop akeneo_job_queue
docker rm -v akeneo_job_queue
```

### Run `php` commands

Sometimes special tasks have to be run within akeneo. They might look like this:

```shell
php bin/console akeneo:batch:job-queue-consumer-daemon
```

In order to execute them these commands have to be run in the `php` service of the Akeneo Cluster.

```shell
APP_ENV=dev docker-compose run --rm php \
    THE_COMMAND_YOU_HAVE_TO_RUN
```

E.g.:

```shell
APP_ENV=dev docker-compose run --rm php \
    php bin/console akeneo:batch:job-queue-consumer-daemon
```

## Create Akeneo-PIM Folder

**The `pim` folder is already part of this repo and some customization might have been done to it. So, only delete the folder if it is really necessary.**

Command to recreate the `pim` folder *after it has been deleted(!)*:

```sh
docker run -it --rm -u www-data -v $(pwd)/pim:/srv/pim -w /srv/pim akeneo/pim-php-dev:5.0 \
    php -d memory_limit=4G /usr/local/bin/composer create-project --prefer-dist \
    akeneo/pim-community-standard /srv/pim "5.0.*@stable"
```
