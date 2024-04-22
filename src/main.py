import re
from pprint import pprint
from src.models.predict import get_embedding


'''
Setup:
- Redis

Steps:
1. Ask user for input regarding today's weather. Ex "Today is raining outside, what should I where?"
2. Extract the weather (using regex)
3. Preform a similarity search with the weather and arbitrary clothing fit from DB
'''


def extract_weather(user_input: str) -> str:
    weather_patterns = r'\b(sunny|cloudy|rainy|raining|partly cloudy|hail|hailing|snowing|snowy|windy|wind)\b'

    matches = [match for match in re.findall(weather_patterns, user_input) if match]

    return matches[0]



def get_user_input() -> str:
    return input("Enter a question regarding clothing: ")


def main() -> None:
    user_input = get_user_input()

    weather = extract_weather(user_input)

    pprint(weather)


if __name__ == "__main__":
    main()
