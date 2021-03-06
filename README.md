# Client Management System (Flask & VueJs)

<a href="https://codeclimate.com/github/KunyuHe/Client-Management-System/maintainability"><img src="https://api.codeclimate.com/v1/badges/d8f1da142654290dc827/maintainability" /></a> [![Codacy Badge](https://app.codacy.com/project/badge/Grade/d87c3f64e7da4a0e83b6c31003e3728e)](https://www.codacy.com/manual/kunyuhe/Client-Management-System?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KunyuHe/Client-Management-System&amp;utm_campaign=Badge_Grade)

This project is a webserver build for facilitating interactions between the Sales and Trading department and its clients. It features pushing trading request notifications from the server to relevant users, emailing clients with attachments, and visualizing client income time series.

**Live demo: http://81.70.5.121/**

**Tech Stack:**

- Back-end: `Flask`
- Front-end: `Vue.js`
- Database: `PostgreSQL`

![Vue Logo](frontend/src/assets/vue-logo.png "Vue Logo") ![Flask Logo](frontend/src/assets/flask-logo.png "Flask Logo")![PSQL Logo](frontend/src/assets/psql-logo.png "PostgresSQL Logo")

## Getting Started

Follow the instructions to get a copy of the project up and running on your local machine for development and testing purposes.

First, install `Git` and navigate to a location on your machine to put this project, and run:

```console
sudo yum install git
git clone https://github.com/KunyuHe/Client-Management-System.git
cd Client-Management-System
```

### Backend

To run the backend properly, please first make sure you have `Docker` installed. Follow the instructions [here](https://docs.docker.com/engine/install/) if it has not been installed yet.

#### Database

In this section we will set up a `Docker` container to host our `PostgreSQL` database and create a `Docker` network to connect it with the container for our `Flask` server.

> An alternative would be install `PostgreSQL` locally and create a database. Follow the instructions [here](https://www.postgresql.org/docs/9.3/tutorial-install.html) and [here](https://www.postgresql.org/docs/9.0/tutorial-createdb.html) respectively. You can skip this section if you choose to go down this road.

Since the webserver runs on `PostgreSQL`, we nee to first pull the `PostgreSQL` image and deploy it. Run:

```console
docker pull postgres
docker run --name <psql-container> -e POSTGRES_PASSWORD=<psql-password> -d <psql-database>
```

Keep `<psql-network-name>`, `<psql-password>`, and `<psql-database>` in mind as we will use them later to configure our `Flask` server.

> `docker pull` can be quite slow for hosts in mainland China. To speed things up, we can use a registry mirror. To set it up, create or modify `/etc/docker/daemon.json` as follows:
>
> ```json
> {
>   "registry-mirrors": ["<your registry mirror url>"]
> }
> ```
>
> For my cloud server in Beijing, China, I used https://registry.docker-cn.com. Run `sudo pkill -SIGHUP dockerd` to reboot `Docker` after the change.

To make sure the `PostgreSQL` container is up and running and the database is successfully created, run the following to check (you can obtain the `<container-id>` from the output of the first command):

 ```console
docker ps
docker exec -it <container-id> psql -U postgres

postgres=# \l
 ```

As we will create another container for the server, and there would be traffic between the two, we need to create a `Docker` network and connect them to it. As the containers would be running on the same `Docker` daemon host, we can simply use a bridge network. Connect the running `PostgreSQL` container to the network.

```console
docker network create <docker-network>
docker network connect <docker-network> <psql-container>
```

#### Flask Server

Before building the `Docker` image, configure the `Flask` server with the correct database URI and secret keys. Open [`backend/config/config.yaml`](./backend/config/config.yaml) and make change to the following sections:

```yaml
COMMON: &common
  DEBUG: False
  SECRET_KEY: <your-key>

  SQLALCHEMY_DATABASE_URI: 'postgresql+psycopg2://postgres:<psql-password>@<psql-container>:5432/<psql-database>'
  SQLALCHEMY_TRACK_MODIFICATIONS: False
  
STAGING: &staging
  <<: *common
  SECRET_KEY: <your-key>

PRODUCTION: &production
  <<: *common
  SECRET_KEY: <your-key>
```

> By default, the app runs in development mode. Make the following changes to the [Dockerfiile](./backend/Dockerfile) to run it in production stage:
>
> ```dockerfile
> # CMD python run.py
> RUN chmod 777 -R ./*
> CMD python run.py
> ```

Run the following under `/backend/` (under the same directory as the [Dockerfiile](./backend/Dockerfile)) to build and run the container for the server, and connect it to the bridge network we set up earlier.

```console
docker build -t <flask-container>:<flask-container-tag> .
docker run -d -p 5000:5000 --network <docker-network> <docker-image-id>
```

`<docker-image-id>` can be retrieved with command `docker images`. The `-p` option maps container ports to host ports. The first port is the port on the host machine, and the one on the right is the port inside the container. We expose port 5000 in the container on port 5000 in the host. To make sure the `Flask` server container is up and running, run `docker ps`.

### Frontend

To set up the frontend properly, make sure you have `Node.js` (with `npm`), `yarn`, and `nginx` installed. Follow the instructions [here](https://nodejs.org/en/download/), [here](https://classic.yarnpkg.com/en/docs/install/#windows-stable), and [here](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) respectively.

Before building for production, edit [`frontend/src/api/api.js`](./frontend/src/api/api.js) and change the variable `url` to http://localhost:port-exposed-earlier. Now, navigate back to `frontend/`. Install the frontend dependencies, complies and minifies for production with:

```console
yarn install
yarn build
```

This would generate a `dist/` directory that can be rendered directly from the `nginx` server. After installing `nginx`, navigate to `/usr/local/etc/nginx/` to edit the file `nginx.conf` and create an entry for our application. An example:

````conf
    server {
        listen       80;
        server_name  localhost;

        access_log  logs/host.access.log  main;

        location / {
            root   html/dist;
            index  index.html index.htm;
        }

        location ~ .*\.(js|css|ico|png|jpg|eot|svg|ttf|woff|html) {
        root html/dist/;
        expires  30d;
    }
````

According to the configuration, we should copy the `dist/` subdirectory to `/usr/local/etc/nginx/html/` and reload `nginx`. Navigate to the target directory and run:

```console
cp -r <your-path-to-project-root>/frontend/dist ./
nginx -s reload
```

Now, you should be able to visit the webserver at http://localhost:80/.

## Features



## License

This project is released under [GNU General Public License v3.0](./LICENSE).