from pprint import pprint
from src.models.predict import get_embedding


def get_user_input() -> str:
    return input("Enter a string: ")


def main() -> None:
    user_input = get_user_input()
    embedding = get_embedding(user_input)
    pprint(embedding)


if __name__ == "__main__":
    main()
