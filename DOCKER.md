# Docker Setup Guide for iFarm

This guide explains how to run iFarm using Docker and Docker Compose for isolated, reproducible development and deployment environments.

## Prerequisites

- **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Compose)
- **Docker Compose**: v1.29+ (included with Docker Desktop)

Verify installation:
```bash
docker --version
docker compose --version
```

## Quick Start

### 1. Clone and navigate to project
```bash
git clone https://github.com/oyeks-ayo/ifarm.git
cd ifarm
```

### 2. Create `.env` file for Docker
```bash
cp .env.example config/.env
```

Edit `config/.env` and set your credentials:
```properties
DATABASE_URL=postgresql://postgres:0000@db:5432/ifarm_db
SECRET_KEY=your_generated_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=1
DB_USER=postgres
DB_PASSWORD=0000
DB_NAME=ifarm_db
DB_PORT=5432
```

### 3. Start services with Docker Compose
```bash
docker compose up -d
```

This will:
- Build the Flask application image
- Start a PostgreSQL database container
- Run Flask app with auto-reload
- Apply database migrations automatically

### 4. Verify services are running
```bash
docker compose ps
```

Expected output:
```
CONTAINER ID   IMAGE           COMMAND                  STATUS
abc123...      ifarm-app       "python run.py"          Up X seconds
def456...      postgres:15...  "postgres"               Up X seconds
```

### 5. Access the application
- **Web App**: http://localhost:5000
- **Database**: localhost:5432 (from host machine)

### 6. View logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f app
docker compose logs -f db
```

### 7. Stop services
```bash
docker compose down
```

To also remove volumes (database data):
```bash
docker compose down -v
```

---

## Development Workflow

### Run Flask shell
```bash
docker compose exec app flask shell
```

### Create database migration
```bash
docker compose exec app flask db migrate -m "Description"
docker compose exec app flask db upgrade
```

### Run Python commands
```bash
docker compose exec app python -c "print('Hello')"
```

### Access PostgreSQL directly
```bash
# Connect with psql (if installed locally)
psql -h localhost -U postgres -d ifarm_db

# Or use Docker container
docker compose exec db psql -U postgres -d ifarm_db
```

### View database via pgAdmin (dev profile)
```bash
docker compose --profile dev up -d
```

Then access pgAdmin at: http://localhost:5050
- Email: `admin@ifarm.local`
- Password: `admin`

To connect in pgAdmin:
- Host: `db`
- Port: `5432`
- Database: `ifarm_db`
- User: `postgres`
- Password: `0000`

### Rebuild Docker image after changes
```bash
docker compose build --no-cache
docker compose up -d
```

---

## Production Deployment

### 1. Update environment variables
Edit `config/.env` with production values:
```properties
DATABASE_URL=postgresql://prod_user:secure_pass@prod.db.host:5432/ifarm_db
SECRET_KEY=generate_strong_secret_key
FLASK_ENV=production
FLASK_DEBUG=0
```

### 2. Build production image
```bash
docker build -t ifarm:latest .
```

### 3. Push to Docker registry (optional)
```bash
docker tag ifarm:latest your-registry/ifarm:latest
docker push your-registry/ifarm:latest
```

### 4. Deploy to production
Use a container orchestration platform:
- **Docker Swarm**: `docker stack deploy -c docker-compose.yml ifarm`
- **Kubernetes**: Convert compose to Kube manifests (use `kompose`)
- **Cloud Platforms**: AWS ECS, Google Cloud Run, Azure Container Instances, Heroku

---

## Troubleshooting

### Port already in use
```bash
# Change port in docker-compose.yml or .env:
APP_PORT=8000
DB_PORT=5433

# Or kill existing process
docker compose down
lsof -i :5000  # Find process using port
kill -9 <PID>
```

### Database connection failed
```bash
# Check if db service is healthy
docker compose ps
docker compose logs db

# Rebuild and restart
docker compose down -v
docker compose build
docker compose up -d
```

### Flask app crashes
```bash
# Check app logs
docker compose logs app

# Re-run migrations
docker compose exec app flask db upgrade

# Rebuild with fresh dependencies
docker compose down
docker compose build --no-cache
docker compose up
```

### Permission denied errors
```bash
# Ensure Docker daemon is running
sudo systemctl start docker  # Linux
# Or restart Docker Desktop  # macOS/Windows
```

---

## Advanced Configuration

### Custom PostgreSQL initialization
Place SQL scripts in `migrations/versions/` or create an `init.sql`:
```bash
mkdir -p docker/postgres-init
# Add *.sql files to be auto-run
```

### Multi-stage builds for optimization
The Dockerfile uses multi-stage builds to:
- Separate build dependencies from runtime
- Reduce final image size
- Improve security

### Health checks
Services have health checks configured:
- Database: `pg_isready` check every 10s
- App: HTTP health endpoint every 30s

### Override compose for local development
Create `docker-compose.override.yml`:
```yaml
version: '3.9'
services:
  app:
    environment:
      FLASK_DEBUG: 1
    volumes:
      - .:/app
```

---

## Cleaning up

### Remove stopped containers
```bash
docker container prune
```

### Remove unused images
```bash
docker image prune
```

### Remove all iFarm containers and volumes
```bash
docker compose down -v --remove-orphans
```

### Complete cleanup (be careful!)
```bash
docker system prune -a --volumes
```

---

## Docker Best Practices Used

✅ **Multi-stage builds** – Smaller final image  
✅ **Non-root user** – Security (appuser:1000)  
✅ **Health checks** – Automated service monitoring  
✅ **Volume mounts** – Persistent data and development workflow  
✅ **Environment variables** – Easy configuration  
✅ **Alpine base images** – Minimal, secure base  
✅ **PYTHONUNBUFFERED** – Real-time log output  
✅ **Layer caching** – Faster rebuilds  

---

## Further Reading

- [Docker Official Docs](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [12 Factor App](https://12factor.net/)
- [Container Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Last Updated**: November 14, 2025
