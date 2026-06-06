FROM eclipse-temurin:17-jdk-jammy AS build
WORKDIR /app
COPY gradlew gradlew
COPY gradle gradle
COPY build.gradle.kts build.gradle.kts
COPY settings.gradle.kts settings.gradle.kts
RUN chmod +x gradlew
COPY src src
RUN ./gradlew bootJar --no-daemon
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /app/build/libs/ /app/libs/
RUN find /app/libs -name "*.jar" -not -name "*-plain.jar" -exec cp {} app.jar \;
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
