import numpy as np
from os import path
import pandas as pd
from tqdm import tqdm
from redis import Redis
from src.models.predict import get_embedding
from redis.commands.search.field import VectorField, TextField


def parse_clothing_articles_csv(

) -> list[dict]:
    clothing_collection = []
    csv_file_path = path.join(path.dirname(path.realpath(__file__)), "../../data", "clothing_articles.csv")

    df = pd.read_csv(csv_file_path)

    for _, row in df.iterrows():
        clothing = row['clothing_articles']
        weather = row['weather']

        item = {
            "Clothing": {
                "clothing_articles": clothing,
                "weather": weather
            }
        }

        clothing_collection.append(item)

    return clothing_collection


def fill_db(
        conn: Redis, clothing_collection: list[dict]
):
    vector_field_name = "weather_vector"
    clothing_field_name = "clothing_articles"

    schema = [
        VectorField(
            vector_field_name,
            "FLAT",
            {"TYPE": "FLOAT32", "DIM": 300, "DISTANCE_METRIC": "COSINE"}
        ),
        TextField(clothing_field_name)
    ]
    conn.ft().create_index(schema)

    for item in tqdm(clothing_collection):
        clothing = item['Clothing']['clothing_articles']
        weather = item['Clothing']['weather']

        weather_embedding = get_embedding(weather)

        if not isinstance(weather_embedding, np.ndarray) or weather_embedding.dtype != np.float32:
            weather_embedding = np.array(weather_embedding, dtype=np.float32)

        conn.hset(clothing, mapping={
            vector_field_name: weather_embedding.tobytes(),
            clothing_field_name: clothing
        })


if __name__ == "__main__":
    redis_conn = Redis(host="localhost", port=6379)
    collection = parse_clothing_articles_csv()
    fill_db(redis_conn, collection)
