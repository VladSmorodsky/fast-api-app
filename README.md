# fast-api-app

This is a FastAPI chat pet project. It provides API for login and register users using JWT. Also application provides
chat functionality with Websocket connection.

## Setup

1. Clone the repo and go to the project root.
2. Create `.env` file from `.env.example` and set values:

- **`SECRET_KEY`**: Django secret key value
- **`ACCESS_TOKEN_TTL`**: JWT access token lifetime in number of minutes.
- **`DB_NAME`**: database name.
- **`DB_USER`**: database user.
- **`DB_PASSWORD`**: database user password.
- **`DB_HOST`**: database host.
- **`DB_PORT`**: database port.
- **`HASH_ALGORITHM`**: algorithm for generating tokens.
- **`DB_URL`**: connection string with next template:
  `<dialect>+<async_version>://<user>:<password>@<host>:<port>/<database_name>`.

3. Run `docker-compose.yml` script:

```shell
docker compose up --build -d
```
