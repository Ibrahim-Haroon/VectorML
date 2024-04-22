from pprint import pprint
import numpy as np
from redis import Redis
from redis.commands.search.query import Query
from src.models.predict import get_embedding


def similarity_search(
        redis_conn: Redis, query_vector: np.ndarray
) -> str:
    IDX_NAME = 'clothing_idx'
    query_vector = query_vector.tobytes()

    query = (
        Query('(*)=>[KNN 1 @vector $vec AS vector_score]')
        .sort_by('vector_score')
        .return_fields('vector_score', '$.clothing_articles')
        .dialect(2)
    )

    results = redis_conn.ft(IDX_NAME).search(query, query_params={'vec': query_vector})

    return ([doc['$.clothing_articles'] for doc in results.docs])[0]


def get_clothing_suggestion(
        weather: str, conn: Redis
) -> str:
    weather_embedding = get_embedding(weather)

    return similarity_search(conn, weather_embedding)


if __name__ == "__main__":
    vectorDB_conn = Redis(host='localhost', port=6379)
    curr_weather = "sunny"
    suggestion = get_clothing_suggestion(curr_weather, vectorDB_conn)
    pprint(suggestion)
