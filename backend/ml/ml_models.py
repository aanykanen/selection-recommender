from tensorflow import keras
from tensorflow.keras import layers


def build_ee_dnn(
    authors_max_len,
    author_vocab_size,
    genres_max_len,
    genres_vocab_size,
    series_max_len,
    series_vocab_size,
    subjects_max_len,
    subjects_vocab_size,
    publisher_max_len,
    publisher_vocab_size,
    n_classes
):
    """
    Builds a deep neural network that solves classification problem with five separate embedding layers as input.

    :param authors_max_len: maximum length of author input
    :param author_vocab_size: number of unique authors in author vocabulary
    :param genres_max_len: maximum length of genres input
    :param genres_vocab_size: number of unique genres in genre vocabulary
    :param series_max_len: maximum length of series input
    :param series_vocab_size: number of unique series in series vocabulary
    :param subjects_max_len: maximum length of subjects input
    :param subjects_vocab_size: number of unique subjects in subject vocabulary
    :param publisher_max_len: maximum length of publisher input
    :param publisher_vocab_size: number of unique publishers in publisher vocabulary
    :param n_classes: number of classes to output
    """

    input_authors = layers.Input(shape=(authors_max_len,))
    embedding_author = layers.Embedding(
        author_vocab_size + 1, 
        50, 
        input_length=authors_max_len, 
        mask_zero=True
        )(input_authors)
    embedding_author = layers.Flatten()(embedding_author)

    input_genres = layers.Input(shape=(genres_max_len,))
    embedding_genres = layers.Embedding(
        genres_vocab_size + 1, 
        50, 
        input_length=genres_max_len, 
        mask_zero=True
        )(input_genres)
    embedding_genres = layers.Flatten()(embedding_genres)

    input_series = layers.Input(shape=(series_max_len,))
    embedding_series = layers.Embedding(
        series_vocab_size + 1, 
        50, 
        input_length=series_max_len, 
        mask_zero=True
        )(input_series)
    embedding_series = layers.Flatten()(embedding_series)

    input_subjects = layers.Input(shape=(subjects_max_len,))
    embedding_subjects = layers.Embedding(
        subjects_vocab_size + 1, 
        50, 
        input_length=subjects_max_len, 
        mask_zero=True
        )(input_subjects)
    embedding_subjects = layers.Flatten()(embedding_subjects)

    input_publishers = layers.Input(shape=(publisher_max_len,))
    embedding_publishers = layers.Embedding(
        publisher_vocab_size + 1, 
        50, 
        input_length=publisher_max_len, 
        mask_zero=True
        )(input_publishers)
    embedding_publishers = layers.Flatten()(embedding_publishers)

    x = layers.Concatenate(axis=1)([
        embedding_author, 
        embedding_genres, 
        embedding_series, 
        embedding_subjects, 
        embedding_publishers])
    x = layers.Dense(100, kernel_initializer='he_uniform', activation='relu')(x)
    x = layers.Dense(50, kernel_initializer='he_uniform', activation='relu')(x)
    x = layers.Dense(n_classes, activation='softmax')(x)

    return keras.Model([input_authors, input_genres, input_series, input_subjects, input_publishers], x)
