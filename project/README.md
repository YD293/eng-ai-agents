
## Requirements

### Start clearml server

1. Install clearml server by following https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_linux_mac/
2. Change CLEARML_API_ACCESS_KEY and CLEARML_API_SECRET_KEY in docker-compose-local.yaml

### Install ollama

1. Install ollama by following https://github.com/ollama/ollama
2. use llama3.1 model: `ollama run llama3.1`

## Run the code by docker compose

### Start docker compose

```bash
docker compose -f docker-compose-local.yaml build
docker compose -f docker-compose-local.yaml up
```

## Or run the code by local

### Install dependencies

```bash
rye sync
```

### ETL

In this step, it will crawl the ros2, nav2, moveit and gazebo github docs, and store the data into MongoDB.

run code by
```bash
rye run python -m crawlers.ros2
```

### Feature Engineering

In this step, it will do the following things:
- Query the documents from MongoDB
- Clean the documents
- Chunk the documents into smaller chunks
- Embed the chunks
- Store the chunks into Qdrant

run code by
```bash
rye run python -m pipelines.feature_engineering
```

### App by Gradio

In this step, it will build a simple app by Gradio to chat with the RAG system.

run code by
```bash
rye run python -m app
```
