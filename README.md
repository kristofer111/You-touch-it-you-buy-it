An ordering system to create and charge orders, validate payments, and send notifications to customers.

### Technologies

- `Flask`
- `PostgreSql`
- `Docker`
- `RabbitMQ`

### Approach

- The system consists of a few small microservices that communicate through network-calls.
- Some network-calls go through RabbitMQ and are event-driven, while others are request/response based.
- SendGrid is used to send email notifications and confirmations to users
- All incoming requests go through a gateway-API which encapsulates the system.
- All services are containerized with Docker.

### Running the Project
 
All services should start when `docker compose up --scale EmailService=2` is run. However, here are a few scenarios to consider.

#### If the "rabbitmq" service initialization hangs when images are not cached

Please run ``docker compose down`` and then `docker compose up --scale EmailService=2` again.

When spinning up all the containers for the first time using ``docker compose up --scale EmailService=2``, the "rabbitmq" service health check might cause rabbitmq to get stuck initializing and hang indefinitely in the terminal, and block the services that depend on it from starting up.

The health check for rabbitmq is configured to start after 35 seconds. This is roughly the amount of time it takes for rabbitmq to get started after running docker compose up for the first time (i.e., after downloading all images from DockerHub).

#### If the "rabbitmq" service initialization hangs when images are already cached

Wait for ~10 seconds. The services that depend on rabbitmq are just waiting for its health check.

If still nothing happens after waiting, please run `docker compose down` and then `docker compose up --scale EmailService=2` again.

### Overview

<img width="75%" alt="Screenshot (984)" src="https://github.com/user-attachments/assets/70b8a977-cae0-4fda-a82f-eb1194927272" />

