# LabCode log server

## How to setup

### Create container

```
docker compose build
docker compose up -d
```

### (Only first time) Initialize database

```
docker compose exec log-server python -m define_db.models
```

### Access to API documents

Access to [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)