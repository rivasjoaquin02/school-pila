# API-REST in Nodejs + Express

<!-- - **typescript**: for the boys -->

-   **nodejs**: for the js runtime
-   **express**: nodejs framework (used for the api)
-   **zod**: for data validation
-   **postgres**: for the relational database

## Docs

You can test it by using the `api.http` file and the vscode extension `humao.rest-client`

## Getting Started

```shell
git clone https://github.com/rivasjoaquin02/school-pila
cd school-pila/api-pila-node

# install dependencies
pnpm install

# run the server
pnpm run start:postgres
```

## Setup of the postgres DB

The Recipe for building the DB is in the `articles.db` file

### External Website

If you use an external website like PlanetScale or Neon you have to create the env variable

-   `POSTGRES_URI`: "postgres:/..."

### DOCKER

1. Install docker
2. Download postgres from the docker hub

```shell
docker pull postgres:latest
```

3. Run the docker image container

-   **set the password**
-   **set the port**

This is important because it has to be on the env variables

-   `POSTGRES_USER`
-   `POSTGRES_PASSWORD`
-   `POSTGRES_DB`
-   `POSTGRES_PORT`
