# 🚀 Event-Driven Customer Segmentation System

A scalable, real-time customer segmentation engine built with Django, Celery, Redis, and WebSockets.

This system is designed to handle high-frequency customer updates, perform efficient segment evaluation, and deliver real-time updates to connected clients.

---

## 🧠 Overview

This project implements a modern **event-driven architecture** for customer segmentation.

Instead of recalculating segments on every update, the system:

* Queues updates using Redis
* Processes them in batches (debounce strategy)
* Computes segment membership efficiently
* Tracks changes using delta updates
* Propagates changes through dependent segments
* Streams updates to the frontend via WebSockets

---

## ⚙️ Tech Stack

| Layer            | Technology                  |
| ---------------- | --------------------------- |
| Backend          | Django                      |
| API              | Django REST Framework       |
| Async Processing | Celery                      |
| Queue / Cache    | Redis                       |
| Realtime         | Django Channels (WebSocket) |
| Database         | PostgreSQL / SQLite         |
| Containerization | Docker                      |

---

## 🏗 Architecture

```text
Customer Update
    ↓
Django Signal
    ↓
Redis Queue (SET → deduplication)
    ↓
Celery Worker (batch processing)
    ↓
Segment Evaluation Engine
    ↓
Delta Calculation (added / removed)
    ↓
Dependency Propagation (Segment graph)
    ↓
WebSocket Broadcast (real-time)
```

---

## ✨ Core Features

### 🔹 Dynamic Segmentation

Segments are defined using flexible JSON-based rules.

### 🔹 Static Segments

Support for manual segments (`is_dynamic = False`) with explicit refresh.

### 🔹 Delta Tracking

Efficient tracking of changes:

* Added users
* Removed users

### 🔹 Batch Processing (Debounce)

Handles high load (e.g. 50K updates) by:

* Deduplicating events in Redis
* Processing updates periodically

### 🔹 Segment Dependencies

Supports cascading updates via parent-child relationships.

### 🔹 Real-Time Updates

WebSocket layer pushes segment changes instantly to the frontend.

### 🔹 Simulation API

Test system behavior by simulating transactions.

---

## 📂 Project Structure

```text
core/
├── models.py             # Database schema (Customer, Segment, etc.)
├── views.py              # API endpoints (simulation, etc.)
├── signals.py            # Event triggers (enqueue updates)
├── tasks.py              # Celery tasks (batch processing)
├── consumers.py          # WebSocket consumers
├── routing.py            # WebSocket routes
│
├── services/
│   ├── segment_engine.py # Core segmentation logic
│   ├── queue.py          # Redis queue layer
│   ├── notifications.py  # WebSocket broadcasting
│   └── campaigns.py      # Campaign trigger logic
```

```
frontend/
├── src/
│   ├── App.css        # Global styles for the main App component
│   ├── App.jsx        # Root React component (main UI logic lives here)
│   ├── api.js         # Axios API configuration (backend communication)
│   ├── assets/        # Static assets (images, icons, etc.)
│   ├── index.css      # Global CSS styles (applied to entire app)
│   └── main.jsx       # Application entry point (ReactDOM render)
│
└── vite.config.js     # Vite configuration (build + dev server settings)
```
---

## 🔄 Segment Evaluation Flow

```text
evaluate_segment(segment_id)
    ↓
Apply rules to customers
    ↓
Compute:
    added = new_ids - old_ids
    removed = old_ids - new_ids
    ↓
Update SegmentMembership
    ↓
Create SegmentDelta
    ↓
Trigger:
    - WebSocket notifications
    - Dependent segments
    - Campaign actions
```

---

## 📡 API Example

### Simulate Customer Transaction

```http
POST /simulate/
```

```json
{
  "id": 1
}
```

➡️ Updates customer data and triggers segmentation pipeline.

---

## ⚡ Realtime Example (Frontend)

```javascript
const socket = new WebSocket("ws://localhost:8000/ws/segments/");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.segment_id === currentSegmentId) {
    setAdded(data.added);
    setRemoved(data.removed);
  }
};
```

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```

Services:

* web (Django)
* redis
* postgres
* celery worker

---

## 🧪 Local Setup

```bash
# create virtual environment
pip install virtualenv
virtualenv .venv
# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# run server
python manage.py runserver

# run celery worker
celery -A core worker -l info
```

---

## ⚠️ Performance Considerations

* Avoid full table scans (`Customer.objects.all()`) at scale
* Move rule evaluation to database-level queries
* Process only affected segments
* Use Redis + batching to prevent overload
* Use Celery for async heavy jobs

---

## 🔮 Future Improvements

* Rule → SQL compiler (query builder)
* Incremental segmentation (no full recomputation)
* Graph-based execution (topological sorting)
* Authenticated WebSocket connections (JWT)
* Monitoring (Prometheus / Grafana)
* Horizontal scaling (multiple workers)

---

## 💡 Use Cases

* Marketing automation platforms
* Customer data platforms (CDP)
* Behavioral segmentation engines
* Real-time personalization systems

---

## 🧑‍💻 Author

Built as a scalable backend system demonstrating:

* Event-driven architecture
* Async processing
* Real-time systems
* Clean service-layer design
