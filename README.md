
## Start clearml server

1. Install clearml server.
2. Change CLEARML_API_ACCESS_KEY and CLEARML_API_SECRET_KEY in docker-compose-local.yaml

### Install ollama

1. Install ollama.
2. use llama3.1 model: `ollama run llama3.1`

## Run the code by docker compose

### Start docker compose

```bash
docker compose -f docker-compose-local.yaml build
docker compose -f docker-compose-local.yaml up
```

### Question and answer

1. Tell me how can I navigate to a specific pose - include replanning aspects in your answer.
![q1](./q1.png)

2. Can you provide me with code for this task?
![q2](./q2.png)
