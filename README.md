![build](https://github.com/Ibrahim-Haroon/VectorML/actions/workflows/ci-pipeline.yml/badge.svg)
# Custom ML model for creating embeddings from text data
## Used to do clothing recommendation based on weather

## GETTING STARTED
### Prerequisites
- Docker

### Docker Installation
- Install Docker from [here](https://docs.docker.com/get-docker/)

### Running the Docker Image
```
docker-compose up --build
```

### Executing the Container
```
docker exec -it vector-ml-server bash
```

### Setup Python Path
```
export PYTHONPATH="/VectorML/src:$PYTHONPATH"
```

### Training the Model
```
python src/models/model.py
```

### Fill the Database
```
python src/vector_db/fill_db.py
```

### Running main.py
```
python src/main.py
```