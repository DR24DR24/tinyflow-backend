# tinyflow-backend

TinyFlow Backend MVP

Components:

- FastAPI REST API
- Celery background workers
- Redis message broker
- Docker Compose deployment

```markdown
## Docker Compose Services

The application is deployed as three Docker containers managed by Docker Compose.

### 1. FastAPI API Container (`tinyflow-api`)

**Purpose:**  
Provides the REST API interface for submitting optimization tasks and checking task status.

**Responsibilities:**

- Receives optimization requests.
- Creates Celery tasks.
- Returns task IDs.
- Provides health check endpoint.

**Port:**

```

8000

````

**Health check:**

```bash
curl http://localhost:8000/health
````

Expected response:

```json
{
  "status": "ok",
  "service": "tinyflow-api",
  "host": "container_id"
}
```

---

### 2. Celery Worker Container (`tinyflow-worker`)

**Purpose:**
Executes long-running background optimization tasks asynchronously.

**Responsibilities:**

* Receives tasks from Redis queue.
* Executes optimization jobs.
* Returns task results.

Currently, optimization is simulated with a 30-second processing delay.
The worker can later be extended with real ML operations:

* model analysis;
* quantization;
* pruning;
* benchmarking;
* deployment generation.

**Check worker status:**

```bash
docker compose logs worker
```

Expected output:

```
celery@container_id ready.

[tasks]
  . tasks.optimize_model
```

**Monitor task execution:**

```bash
docker compose logs -f worker
```

Example:

```
Task tasks.optimize_model[...] received

Starting optimization: resnet18.onnx

Optimization finished

Task tasks.optimize_model[...] succeeded
```

---

### 3. Redis Container (`tinyflow-redis`)

**Purpose:**
Provides a message broker and result backend for Celery.

**Responsibilities:**

* Stores queued optimization tasks.
* Transfers tasks from FastAPI to Celery Worker.
* Stores task execution results.

**Port:**

```
6379
```

**Check Redis container status:**

```bash
docker compose ps
```

Expected output:

```
tinyflow-api       running
tinyflow-worker    running
tinyflow-redis     running
```

**Check Redis availability:**

```bash
docker exec -it tinyflow-redis redis-cli ping
```

Expected response:

```
PONG
```

---

## Start All Containers

Build and run the complete application:

```bash
docker compose up --build
```

## Stop All Containers

```bash
docker compose down
```

## View Running Containers

```bash
docker compose ps
```

## View All Logs

```bash
docker compose logs
```

## Follow Logs in Real Time

```bash
docker compose logs -f
```

```
```
