from pprint import pprint
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.data_processing.preprocess import get_padded_sequences_and_tokenizer
from os import path


def get_embedding(
        string: str,
        save_path: str = path.join(path.dirname(path.realpath(__file__)), "../", "other/ml_model.keras")
) -> np.ndarray:
    model = tf.keras.models.load_model(save_path)

    padded_sequences, tokenizer = get_padded_sequences_and_tokenizer()
    seq = tokenizer.texts_to_sequences([string])
    pad = pad_sequences(seq, maxlen=(padded_sequences.shape[1]))

    embedding_layer = model.layers[0]
    embeddings = embedding_layer(pad)

    return (embeddings.numpy())[0][0]


def main(

) -> None:
    embedding = get_embedding("foo")

    print(f"len of embedding is {len(embedding)}")
    pprint(embedding)


if __name__ == "__main__":
    main()
