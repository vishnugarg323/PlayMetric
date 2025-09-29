FROM maven:3.8.4-openjdk-17 AS builder
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

FROM openjdk:17-slim
WORKDIR /app
COPY --from=builder /app/playmetric-test-util/target/playmetric-test-util-*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
