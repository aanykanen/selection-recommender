import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

from pandas import DataFrame
from sklearn import metrics


def features_to_text(list_of_indices, reverse_word_map):
    """
    Returns labels of features given array of ids.

    :param list_of_indices: list of index values found in word map of tokenizer
    :param reverse_word_map: dictionary consisting of tokenizer map reversed
    """
    words = [reverse_word_map.get(letter) for letter in list_of_indices]
    return(words)


def save_confusion_matrix(cf, name):
    """
    Saves confusion matrix to metrics folder.

    :param cf: confusion matrix produced by sklearn.metrics.confusion_matrix
    :param name: filename for saved file
    """
    cols = [0, 1]
    df_cm = DataFrame(cf, index=cols, columns=cols)
    sn.heatmap(df_cm, annot=True, fmt='g', cmap='Greys').get_figure()
    plt.savefig(f'metrics/{name}.png', dpi=400)
    plt.clf()


def test_model(model, X_test, y_test, name):
    """
    Tests model and saves report of test as confusion matrix.

    :param model: ML model to be tested
    :param X_test: test data
    :param y_test: test data labels
    :param name: name of ML model
    """
    name = name.lower().replace(' ', '_')

    if 'lightgbm' in name:
        y_pred = model.predict(X_test, num_iteration=model.best_iteration)
        plt.hist(y_pred, 20)
        plt.savefig('metrics/lightgbm_histogram.png')
        plt.clf()
        y_pred = y_pred.round(0).astype(int)
    else:
        y_pred = model.predict(X_test)

    if name == 'dnn_entity_embeddings':
        y_pred = np.argmax(y_pred, axis=1)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    confusion_matrix = metrics.confusion_matrix(y_test, y_pred)

    print(f'{name} accuracy: {round(accuracy * 100, 2)}%')
    print(f'Confusion matrix: {confusion_matrix}')
    save_confusion_matrix(confusion_matrix, name)

    with open('metrics/accuracies.csv', 'a') as f:
        f.write(f'{name},{round(accuracy * 100, 2)}\n')
