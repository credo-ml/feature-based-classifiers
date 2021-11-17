import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import os
from joblib import dump, load
from function import augment_train_data, computeZM, read_img
from sklearn import svm
from sklearn.svm import NuSVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from link_paths import path_save_model


def create_model(images, targets):
    rs = np.random.randint(100)
    images_train4, images_test4, targets_train4, targets_test4 = train_test_split(images, targets, test_size=0.2,
                                                                                  stratify=targets, random_state=rs)
    images_train4, targets_train4 = augment_train_data(images_train4, targets_train4, augconf=[0, 4, 12, 0])
    X_train4, y_train4 = computeZM(images_train4, targets_train4)
    X_test4, y_test4 = computeZM(images_test4, targets_test4)

    name, scaler = 'StandardScaler', StandardScaler()
    scaler = scaler.fit(X_train4, y_train4)
    X_train4 = scaler.transform(X_train4)
    X_test4 = scaler.transform(X_test4)

    c1 = MLPClassifier(solver='adam', activation='relu', hidden_layer_sizes=(100, 100),
                       max_iter=10000)
    c2 = NuSVC(gamma=0.1, kernel='rbf', nu=0.05)
    c3 = svm.SVC(C=700, gamma=0.08, kernel='rbf')
    clf = VotingClassifier(estimators=[('c1', c1), ('c2', c2), ('c3', c3)],
                           weights=(4, 8, 8))
    clf.fit(X_train4, y_train4)

    clf1=clf
    y_pred = clf1.predict(X_test4)
    print('Dokładność: {:.2f}%'.format(100 * accuracy_score(y_test4, y_pred)))

    name2 = "vot"


    filename = os.path.join(path_save_model, name2+".pkl")
    filename2 = os.path.join(path_save_model, name2+"_scaler.pkl")
    dump(clf, filename)
    dump(scaler, filename2)

def main():
    images,targets = read_img()
    create_model(images, targets)


if __name__ == '__main__':
    main()