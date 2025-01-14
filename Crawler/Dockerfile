FROM maven:3.8.4-openjdk-17-slim AS build

WORKDIR /app

COPY pom.xml .

RUN mvn dependency:go-offline

COPY src ./src

RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-slim

WORKDIR /app

COPY --from=build /app/target/crawler.jar crawler.jar

COPY --from=build /app/target/libs ./libs

ENTRYPOINT ["java", "-cp", "crawler.jar:libs/*", "org.crawler.Main"]
