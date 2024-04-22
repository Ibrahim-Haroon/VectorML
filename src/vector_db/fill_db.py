"""
This module is responsible for filling the database with the clothing articles and creating the search index
"""
from os import path
import pandas as pd
from tqdm import tqdm
from redis import Redis
from src.models.predict import get_embedding
from redis.commands.search.field import VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType


def parse_clothing_articles_csv(

) -> list[dict]:
    """
    @purpose: This function is responsible for parsing the clothing articles csv file
    :rtype: list[dict]
    :return: list of clothing articles
    """
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
) -> None:
    """
    @purpose: This function is responsible for filling the database with the clothing articles
    :param conn: db connection
    :param clothing_collection: list of clothing articles
    :rtype: None
    :return: None
    """
    vector_field_name = "weather_vector"
    clothing_field_name = "clothing_articles"

    pipeline = conn.pipeline(transaction=True)

    for item in tqdm(clothing_collection):
        weather_description = item['Clothing']['weather']
        clothing_articles = item['Clothing']['clothing_articles']

        weather_embedding = get_embedding(weather_description)

        key = f"clothing:{weather_description.replace(' ', '_')}"

        init_object = {
            clothing_field_name: clothing_articles,
            vector_field_name: weather_embedding.tolist()
        }

        pipeline.json().set(key, '$', init_object)

    pipeline.execute()
    print("Data has been saved to Redis!")


def create_search_index(
        conn: Redis
) -> None:
    """
    @purpose: This function is responsible for creating the search index
    :param conn: db connection
    :return: None
    """
    IDX_NAME = 'clothing_idx'
    schema = (
        VectorField('$.weather_vector', 'FLAT', {
            'TYPE': 'FLOAT32',
            'DIM': 300,
            'DISTANCE_METRIC': 'COSINE',
        }, as_name='vector')
    )
    definition = IndexDefinition(prefix=['clothing:'], index_type=IndexType.JSON)
    conn.ft(IDX_NAME).create_index(fields=schema, definition=definition)
    print('Index created successfully!')


if __name__ == "__main__":
    redis_conn = Redis(host="redis", port=6379)
    redis_conn.flushall()
    collection = parse_clothing_articles_csv()
    fill_db(redis_conn, collection)
    create_search_index(redis_conn)
