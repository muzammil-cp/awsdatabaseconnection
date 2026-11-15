# AWS database connection demos

This repository contains two separate demos:

- `databasedemo/`: Spring Boot REST API backed by MySQL or Amazon RDS for MySQL.
- `pythondynamodb/`: Python script that creates and uses a DynamoDB table.
- `mysqldatabase/`: local MySQL plus the Spring Boot app using Docker Compose.

## Run the MySQL app locally

From the repository root, set a local password and start both containers. In PowerShell:

```powershell
$securePassword = Read-Host "Choose a local MySQL password" -AsSecureString
$env:MYSQL_ROOT_PASSWORD = [System.Net.NetworkCredential]::new("", $securePassword).Password
docker compose -f mysqldatabase/docker-compose.yml up --build
```

Compose builds the app from `databasedemo/`, waits for MySQL to accept connections, and serves the API at `http://localhost:8080/api/items`. The local database port is bound to localhost only.

Create an item and list items:

```powershell
curl.exe -X POST http://localhost:8080/api/items -H "Content-Type: application/json" -d '{ "name": "Demo item" }'
curl.exe http://localhost:8080/api/items
```

Stop the containers with `docker compose -f mysqldatabase/docker-compose.yml down`. The named volume keeps local database data. Then clear the password from your PowerShell session with `Remove-Item Env:MYSQL_ROOT_PASSWORD`.

## Connect the app to Amazon RDS for MySQL

1. In RDS, confirm the database is available and copy its endpoint and port. This app expects MySQL and uses database `databasedemo`; `DB_HOST` must include the port, usually `3306`.
2. Create the database and a dedicated app user using an authorized MySQL administrator. Replace the password placeholder with a strong password; do not commit it.

```sql
CREATE DATABASE IF NOT EXISTS databasedemo;
CREATE USER 'appuser'@'%' IDENTIFIED BY 'REPLACE_WITH_A_STRONG_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX ON databasedemo.* TO 'appuser'@'%';
```

If the user already exists, use `ALTER USER` to update its password instead of running `CREATE USER` again. Restrict network access with the RDS security group; never allow port 3306 from `0.0.0.0/0`.

Build the current source image from the repository root:

```bash
docker build -t databasedemo:local ./databasedemo
```

Run the app on Linux/macOS, replacing the placeholders:

```bash
docker run --rm -p 8080:8080 \
  -e DB_HOST="YOUR_RDS_ENDPOINT:3306" \
  -e DB_USER="appuser" \
  -e DB_PASSWORD="YOUR_APP_PASSWORD" \
  databasedemo:local
```

In PowerShell, put the same command on one line. Open `http://localhost:8080/api/items`; use the POST and GET examples above. The datasource requires TLS. The container must have network access to RDS, and the RDS security group must allow TCP 3306 from the container host or its security group.

## DynamoDB demo

See [`pythondynamodb/README.md`](pythondynamodb/README.md) for secure AWS credential setup and required IAM permissions. The demo creates a table in the selected AWS Region and performs a sample write and read.
