"""
This module contains the code for training a simple embedding model.
"""
import numpy as np
from os import path
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense
from src.data_processing.preprocess import get_padded_sequences_and_tokenizer


def build_model(
        vocab_size: int,
        output_dim: int = 300,
) -> Sequential:
    """
    @purpose: Build a simple embedding model
    :param vocab_size: size of the vocabulary (number of unique words)
    :param output_dim: dimension of the vector embedding
    :rtype: Sequential
    :return: Sequential model
    """
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=output_dim),
        Flatten(),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy')

    model.summary()

    return model


def train_model(
        model: Sequential,
        input_sequences: np.ndarray,
        target_sequences: np.ndarray,
        save_path: str,
        epochs: int = 10,
        batch_size: int = 64,
        validation_split: float = 0.2
) -> None:
    """
    @purpose: Train the model
    :param model: Sequential
    :param input_sequences: np.ndarray which contains the input sequences
    :param target_sequences: np.ndarray which contains the target sequences
    :param save_path: str path to save the model
    :param epochs: number of times model is trained on the entire dataset
    :param batch_size: number of samples per gradient update
    :param validation_split: fraction of the training data to be used as validation data
    :rtype: None
    :return: None
    """
    model.fit(
        input_sequences,
        target_sequences,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split
    )

    model.save(save_path)


def main(

) -> None:
    save_path = path.join(path.dirname(path.realpath(__file__)), "embedding_model.keras")

    padded_sequences, tokenizer = get_padded_sequences_and_tokenizer()
    vocab_size = len(tokenizer.word_index) + 1
    input_sequences = np.array(padded_sequences, dtype='float32')
    target_sequences = np.zeros((input_sequences.shape[0], 1), dtype='float32')

    model = build_model(vocab_size)
    train_model(model, input_sequences, target_sequences, save_path)


if __name__ == '__main__':
    main()
