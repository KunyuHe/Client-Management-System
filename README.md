# Client Management System (Flask & VueJs)

<a href="https://codeclimate.com/github/KunyuHe/Client-Management-System/maintainability"><img src="https://api.codeclimate.com/v1/badges/d8f1da142654290dc827/maintainability" /></a> [![Codacy Badge](https://app.codacy.com/project/badge/Grade/d87c3f64e7da4a0e83b6c31003e3728e)](https://www.codacy.com/manual/kunyuhe/Client-Management-System?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KunyuHe/Client-Management-System&amp;utm_campaign=Badge_Grade)

This project is a webserver build for facilitating interactions between the Sales and Trading department and its clients. It features pushing trading request notifications from the server to relevant users, emailing clients with attachments, and visualizing client income time series.

**Tech Stack:**

- Back-end: `Flask`
- Front-end: `Vue.js`
- Database: `PostgresSQL`

![Vue Logo](frontend/src/assets/vue-logo.png "Vue Logo") ![Flask Logo](frontend/src/assets/flask-logo.png "Flask Logo")![PSQL Logo](frontend/src/assets/psql-logo.png "PostgresSQL Logo")

## Getting Started

Follow the instructions to get a copy of the project up and running on your local machine for development and testing purposes.

First, navigate to a location on your machine to put this project, and run:

```console
git clone https://github.com/KunyuHe/Client-Management-System.git
cd Client-Management-System
```

### Backend

To run the backend properly, please first make sure you have `Docker Engine` installed. Follow the instructions [here](https://docs.docker.com/engine/install/) if it is not installed yet.

#### Database

insecure