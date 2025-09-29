FROM maven:3.8.4-openjdk-17 AS builder
WORKDIR /app
COPY ./pom.xml ./pom.xml
COPY ./playmetric-service/pom.xml ./playmetric-service/pom.xml
RUN mvn -f ./playmetric-service/pom.xml dependency:go-offline

COPY ./playmetric-service/src ./playmetric-service/src
RUN mvn -f ./playmetric-service/pom.xml clean package -DskipTests

FROM openjdk:17-slim
WORKDIR /app
COPY --from=builder /app/playmetric-service/target/playmetric-service.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
