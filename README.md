# Client Management System (Flask & VueJs)

<a href="https://codeclimate.com/github/KunyuHe/Client-Management-System/maintainability"><img src="https://api.codeclimate.com/v1/badges/d8f1da142654290dc827/maintainability" /></a> [![Codacy Badge](https://app.codacy.com/project/badge/Grade/d87c3f64e7da4a0e83b6c31003e3728e)](https://www.codacy.com/manual/kunyuhe/Client-Management-System?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KunyuHe/Client-Management-System&amp;utm_campaign=Badge_Grade)

This project is a webserver build for facilitating interactions between the Sales and Trading department and its clients. It features pushing trading request notifications from the server to relevant users, emailing clients with attachments, and visualizing client income time series.

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

To run the backend properly, please first make sure you have `Docker Engine` installed. Follow the instructions [here](https://docs.docker.com/engine/install/) if it is not installed yet.

#### Database

Since the webserver runs on `PostgreSQL`, we nee to first pull the `PostgreSQL` image and deploy it. Run:

```console
docker pull postgres
docker run --name <psql-container> -e POSTGRES_PASSWORD=<psql-password> -d <psql-database>
```

Keep `<psql-network-name>`, `<psql-password>`, and `<psql-database>` in mind as we will use them later to configure our `Flask` server.

To make sure the `PostgreSQL` container is up and running and the database is successfully created, run the following to check (you can obtain the `<container-id>` from the output of the first command):

 ```console
docker ps
docker exec -it <container-id> psql -U postgres

postgres=# \l
 ```

Use `\q` to quit `psql`.

As we will create another container for the server, and there would be traffic between the two, we need to create a `Docker` network and connect them to it. As the containers would be running on the same Docker daemon host, we can simply use a bridge network. Connect the running `psql` container to the network.

```console
docker network create <docker-network>
docker network connect <docker-network> <psql-container>
```

