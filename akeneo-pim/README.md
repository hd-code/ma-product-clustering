# Akeneo PIM

## Requirements

- docker 19+
- docker-compose 1.24+
- make

If you are on linux, check if your user has the correct `uid=1000` and `gid=1000`. If not, setup a corresponding user, clone the repo with it and run it only with this user account (see [Use correct user and group](#use-correct-user-and-group-linux-only))!

## Installation and Usage

The script `akeneo.sh` bundles all important commands.

If you run it without arguments, it will tell you how to use it:

```sh
sh akeneo.sh
```

E.g. to create a new instance of Akeneo PIM, run `sh akeneo.sh setup`.

## Troubleshooting

### Use correct user and group (linux-only)

Check your user and group id:

```sh
id
```

If they are not `1000`, you need to create a special user and user group with this id. To do so, follow these steps:

1. Create group `akeneo` and user `akeneo`:

```sh
sudo groupadd -g 1000 akeneo
sudo useradd akeneo -u 1000 -g 1000 -s /bin/bash
```

2. (optional) Disable password for user `akeneo`:

```shell
sudo passwd -d akeneo
```

3. Add user `akeneo` to group `docker` to run docker containers with this user:

```shell
sudo usermod -a -G docker akeneo
```

Now, always remember to run all commands in this repo as user `akeneo`!

```sh
su akeneo
```

### Permissions of yarn Image

During the installation the following error may occur: `EACCES: permission denied, mkdir '/home/node/.yarn/v6'`

If that happens, the permissions for the yarn directory have to be changed. Just run this command in the `pim` directory:

```sh
docker-compose run -u root node chown -R node:node /home/node/.yarn
```
