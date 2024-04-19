import tensorflow as tf
import nltk
from nltk.tokenize import word_tokenize
import string
from os import path
import pandas as pd


def print_padded_sequences(padded_sequences) -> None:
    df_sequences = pd.DataFrame(padded_sequences)
    print(df_sequences.head())


def clean_text(text) -> list[str]:
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)

    return words


def build_vocab(tokenized_lines) -> list[list[int]] and tf.keras.preprocessing.text.Tokenizer:
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(tokenized_lines)
    sequences = tokenizer.texts_to_sequences(tokenized_lines)

    return sequences, tokenizer


def get_padded_sequences_and_tokenizer() -> tf.Tensor and tf.keras.preprocessing.text.Tokenizer:
    file_path = path.join(path.dirname(path.realpath(__file__)), '../../data', 'raw')
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    tokenized_lines = [clean_text(line) for line in lines]

    sequences, tokenizer = build_vocab(tokenized_lines)
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, padding='post')

    return padded_sequences, tokenizer


def save_padded_sequences(padded_sequences) -> None:
    processed_data_path = path.join(path.dirname(path.realpath(__file__)), '../../data', 'processed.csv')
    df_sequences = pd.DataFrame(padded_sequences)
    df_sequences.to_csv(processed_data_path, index=False)
    print(f"Data saved to {processed_data_path}")


def main() -> None:
    padded_sequences, _ = get_padded_sequences_and_tokenizer()
    print_padded_sequences(padded_sequences)
    save_padded_sequences(padded_sequences)


if __name__ == '__main__':
    nltk.download('punkt')
    main()
