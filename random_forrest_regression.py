from shared.queueUtils import *
from shared.board import *

mysql_con = getMysqlConnection()
cursor = mysql_con.cursor()
query = 'select * from samples_3 where wins+loses > 25'
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

data_count = int(len(training_data_list) * 0.80)
training_labels = result_list[:data_count]
training_features = feature_list[:data_count]
testing_labels = result_list[data_count:]
testing_features = feature_list[data_count:]

from sklearn.ensemble import RandomForestRegressor

clf = RandomForestRegressor(n_estimators=10)
clf = clf.fit(training_features, training_labels)

#from sklearn.neighbors import KNeighborsRegressor
#clf = KNeighborsRegressor(n_neighbors=3)

#from sklearn import linear_model
#clf = linear_model.Lasso(alpha=0.1)

clf.fit(training_features, training_labels)
results = clf.predict(testing_features)

totalWrong = 0
totalGood = 0
for i, result in enumerate(results):
     print("diff: " + str(abs(testing_labels[i]-result)) + " Got: " + str(result) + ". Expected: " + str(testing_labels[i]))
     print(testing_features[i])
     totalWrong += abs(testing_labels[i]-result)

print(totalWrong / len(results))