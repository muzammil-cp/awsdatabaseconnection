# Stage 1: Build the application using Maven
FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app

COPY mvnw pom.xml ./
COPY .mvn .mvn
COPY src src

# GitHub does not preserve executable bits for every wrapper checkout.
RUN chmod +x mvnw && ./mvnw --batch-mode clean package -DskipTests

# Stage 2: Run the application
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
