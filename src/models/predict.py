"""
This module is used to predict the embedding of a string using the trained model.
"""
from os import path
import numpy as np
from pprint import pprint
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.data_processing.preprocess import get_padded_sequences_and_tokenizer



def get_embedding(
        string: str,
        save_path: str = path.join(path.dirname(path.realpath(__file__)), "embedding_model.keras")
) -> np.ndarray:
    """
    @purpose: Get the embedding of a string
    :param string: word to get the embedding of
    :param save_path: path to the saved model
    :rtype: np.ndarray
    :return: vector embedding
    """
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
