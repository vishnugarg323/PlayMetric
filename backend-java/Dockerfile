
FROM eclipse-temurin:21-jdk-alpine
WORKDIR /app
# Install Maven
RUN apk add --no-cache maven
COPY . .
RUN mvn clean package -DskipTests
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "target/playmetric-parent-1.0-SNAPSHOT.jar"]

