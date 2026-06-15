# One-command production deployment

This package is configured so that the React frontend is built inside Docker
and copied into the Spring Boot application before the JAR is created.

Because the existing nginx configuration already forwards the website to
`127.0.0.1:8080`, nginx does not need a separate frontend directory or a manual
`location /` change. Spring Boot now serves the Vite-generated `index.html`,
JavaScript, CSS, and images itself.

## Deploy

Extract the ZIP as your normal server user, enter the extracted directory, and
run:

```bash
chmod +x start-prod.sh
./start-prod.sh
```

The script:

1. checks Docker and Docker Compose;
2. repairs the runtime-directory permissions with sudo when necessary;
3. preserves an existing `backend_server/webapp/db/users.db` database;
4. builds the React frontend in a Node 22 Docker stage;
5. embeds `frontend/dist` into the Spring Boot JAR;
6. builds and starts the Java and Python containers;
7. checks the backend health endpoint;
8. verifies that `/` contains a Vite JavaScript asset rather than the old
   placeholder page.

The first build needs internet access to pull Docker images and dependencies.

## Existing nginx requirement

The server must already proxy the domain to:

```text
http://127.0.0.1:8080
```

That is the setup which previously displayed the rotating Neuroshima
placeholder. The same proxy will now display the React application, so no nginx
edit is necessary.

## Stop

```bash
./stop-prod.sh
```

## Update later

Replace the project source with the updated copy while preserving:

```text
backend_server/webapp/db/users.db
```

Then run `./start-prod.sh` again. Docker will rebuild changed frontend or backend
layers.
