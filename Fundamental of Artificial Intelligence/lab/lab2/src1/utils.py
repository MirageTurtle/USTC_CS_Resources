import numpy as np
def get_acc(y, pred):
    return np.sum(y == pred) / len(y)


def load_decisiontree_dataset():
    train_data = np.loadtxt('dataset/dt/dt_train.data', delimiter=',', dtype='int64')
    test_data = np.loadtxt('dataset/dt/dt_test.data', delimiter=',', dtype='int64')
    train_features = train_data[:,1:]
    train_labels = train_data[:,0]
    test_features = test_data[:,1:]
    test_labels = test_data[:,0]

    return train_features, train_labels, test_features, test_labels

def load_svm_dataset():
    train_features = np.loadtxt('dataset/svm/svm_train_data.csv', delimiter=',', skiprows=1)
    train_labels = np.loadtxt('dataset/svm/svm_train_label.csv', delimiter=',', skiprows=1, dtype=np.int32)
    test_features = np.loadtxt('dataset/svm/svm_test_data.csv', delimiter=',', skiprows=1)
    test_labels = np.loadtxt('dataset/svm/svm_test_label.csv', delimiter=',', skiprows=1, dtype=np.int32)

    return train_features, train_labels, test_features, test_labels