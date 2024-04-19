from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense
from src.data_processing.preprocess import get_padded_sequences_and_tokenizer
import numpy as np
from os import path


def build_model(
        vocab_size: int,
        output_dim: int = 300,
) -> Sequential:
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
