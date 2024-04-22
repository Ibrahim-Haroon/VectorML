from pprint import pprint
import numpy as np
from redis import Redis
from redis.commands.search.query import Query
from src.models.predict import get_embedding


def similarity_search(conn: Redis, query_vector: np.ndarray):
    query = (
        Query(f"(@weather_vector:{{ $vec }})=>[KNN 1 @weather_vector $vec as score]")
        .sort_by("score")
        .return_fields("clothing_articles", "weather_vector", "score")
        .paging(0, 1)
        .dialect(2)
    )

    query_params = {"vec": query_vector.tobytes()}

    return conn.ft("idx").search(query, query_params).docs


def get_clothing_suggestion(weather: str, conn: Redis):
    weather_embedding = get_embedding(weather)

    return similarity_search(conn, weather_embedding)


if __name__ == "__main__":
    vectorDB_conn = Redis(host='localhost', port=6379)
    curr_weather = "rainy"
    suggestion = get_clothing_suggestion(curr_weather, vectorDB_conn)
    pprint(suggestion)
