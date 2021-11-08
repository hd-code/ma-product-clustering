# adesso Product Clusterer

This project contains the master thesis of [Hannes Dröse](mailto:hannes.droese@adesso.de). It implements a web service, that clusters similar products together. These clusters are then used for product recommendations, better search results and more.

## Installation & Usage

To run the services [Docker](https://www.docker.com) is required, so please install it on your machine.

Now all services can be run from the command line by typing:

```sh
docker-compose up
```

This starts the following services:

| Name            | Url                     | Comment |
|-|-|----|
| Akeneo Service  | <http://localhost:????> | provides the product data from IceCat |
| Cluster Service | <http://localhost:????> | REST-API that performs the clustering and provides the results |
| Web Service     | <http://localhost:????> | serves a web frontend to see the services in action |

To stop all services run:

```sh
docker-compose down
```
