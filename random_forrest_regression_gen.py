from shared.queueUtils import *
from shared.board import *

mysql_con = getMysqlConnection()
cursor = mysql_con.cursor()
query = 'select * from samples_3 where wins+loses > 50'
cursor.execute(query)
training_data_list = cursor.fetchall()

import random
random.shuffle(training_data_list)

cursor.close()
mysql_con.commit()

feature_list = []
result_list = []
for training_data in training_data_list:
    hex = training_data[0]

    features = []
    for c in hex:
        features.append(int(c, 16))
    feature_list.append(features)
    result_list.append(training_data[1] / (training_data[1] + training_data[2]))


from sklearn.ensemble import RandomForestRegressor

clf = RandomForestRegressor(n_estimators=10)
clf = clf.fit(feature_list, result_list)

import pickle
clr_f = open("classifiers/sample3.pickle", "wb")
pickle.dump(clf, clr_f)