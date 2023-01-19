import pandas as pd
from sklearn import  preprocessing
import os ,datetime


def fill_dic(input_list, out_dic, csv_file_name, row_name):
    for index, i in enumerate(csv_file_name[row_name]):
        dic_key = i
        if type(dic_key) == float:
            dic_key = f'None{index}'
        out_dic[dic_key] = input_list[index]

    return out_dic


def save_to_csv(car_info, csv_file_name):
        df = pd.DataFrame.from_dict(car_info, orient='index', )
        df = df.transpose()
        if os.path.isfile(f'{csv_file_name}.csv'):df.to_csv(f'{csv_file_name}.csv',mode='a',header=False, index=0)
        else:df.to_csv(f'{csv_file_name}.csv',index=0)


car_brand_dic = {}
car_model_dic = {}
car_gear_dic = {}
car_city_dic = {}
car_address_dic = {}
car_date_dic = {}

with_price = pd.read_csv("to_use_for_random_forest_with_price.csv")
without_price = pd.read_csv("to_use_for_random_forest_without_price.csv")

with_price = with_price.append(without_price)
with_price = with_price.drop(with_price.columns[0],axis=1)
with_price = with_price.sample(frac=1).reset_index(drop=True)
cars_without_labels = with_price.drop('price',axis=1)
price = with_price['price']

import random
random.seed(100)
from sklearn.model_selection import train_test_split
data_train, data_test, labels_train, labels_test = train_test_split(cars_without_labels, price, test_size=0.20, random_state=100)



# ## Random Forest

from sklearn.ensemble import RandomForestClassifier
RFmodel = RandomForestClassifier()
RFmodel.fit(data_train, labels_train)
rf_pred_label = RFmodel.predict(data_test)



from sklearn.metrics import confusion_matrix,accuracy_score
cm2 = confusion_matrix(labels_test,rf_pred_label)
print(cm2)
print(accuracy_score(labels_test,rf_pred_label))


import pickle
file_name = "RandomForestModel.sav"
pickle.dump(RFmodel,open(file_name,'wb'))
