import re
from redis import Redis
from src.vector_db.recommendation_engine import get_clothing_suggestion


def extract_weather(user_input: str) -> str:
    weather_patterns = r'\b(sunny|cloudy|rainy|raining|partly cloudy|hail|hailing|snowing|snowy|windy|wind)\b'

    matches = [match for match in re.findall(weather_patterns, user_input) if match]

    return matches[0]


def get_user_input() -> str:
    return input("Enter a question regarding clothing: ")


def main(db_conn: Redis) -> None:
    user_input = get_user_input()

    weather = extract_weather(user_input)

    suggestion = get_clothing_suggestion(weather, db_conn)

    print(f"It is recommended to wear the following clothing: {suggestion}")


if __name__ == "__main__":
    vectorDB_conn = Redis(host='localhost', port=6379)
    main(vectorDB_conn)
