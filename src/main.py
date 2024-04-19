from src.models.predict import get_embedding


def get_user_input() -> str:
    return input("Enter a string: ")


def main() -> None:
    embedding = get_embedding("foo")


if __name__ == "__main__":
    main()
