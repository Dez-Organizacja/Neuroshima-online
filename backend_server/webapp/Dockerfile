# syntax=docker/dockerfile:1

# Build the browser frontend first. The resulting Vite files are embedded in
# the Spring Boot JAR, so the existing nginx reverse proxy can keep forwarding
# all requests to 127.0.0.1:8080.
FROM node:22-alpine AS frontend-build
WORKDIR /frontend
ENV ELECTRON_SKIP_BINARY_DOWNLOAD=1

COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npm run build

FROM eclipse-temurin:17-jdk-jammy AS backend-build
WORKDIR /app

COPY backend_server/webapp/gradlew gradlew
COPY backend_server/webapp/gradle gradle
COPY backend_server/webapp/build.gradle.kts build.gradle.kts
COPY backend_server/webapp/settings.gradle.kts settings.gradle.kts
RUN chmod +x gradlew

RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew --no-daemon dependencies || true

COPY backend_server/webapp/src src

# Remove the old placeholder HTML and replace it with the actual React build.
RUN rm -rf src/main/resources/static \
    && mkdir -p src/main/resources/static
COPY --from=frontend-build /frontend/dist/ /app/src/main/resources/static/

RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew bootJar --no-daemon

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=backend-build /app/build/libs/ /app/libs/
RUN find /app/libs -name "*.jar" -not -name "*-plain.jar" -exec cp {} app.jar \;
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
