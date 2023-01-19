import pandas as pd
from sklearn import  preprocessing
import os ,datetime ,pickle, random
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split

class random_forest():
    def __init__(self):       
        self.with_price = pd.read_csv("random_forest_data_with_price.csv")
        self.without_price = pd.read_csv("random_forest_data_without_price.csv")
        self.cars_without_labels = None
        self.price = None
        self.data_train = None 
        self.data_test = None
        self.labels_train = None 
        self.labels_test = None
        self.RFmodel = None
        self.rf_pred_label = None
        random.seed(100)

    def make_df(self): 
        self.with_price = self.with_price.append(self.without_price)
        self.with_price = self.with_price.drop(self.with_price.columns[0],axis=1)
        self.with_price = self.with_price.sample(frac=1).reset_index(drop=True)
        self.cars_without_labels = self.with_price.drop('price',axis=1)
        self.price = self.with_price['price']
        
    def train_model(self):
        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(self.cars_without_labels, self.price, test_size=0.20, random_state=100)
        self.RFmodel = RandomForestClassifier()
        self.RFmodel.fit(self.data_train, self.labels_train)
        self.rf_pred_label = self.RFmodel.predict(self.data_test)

    def check_price(self):
        cm2 = confusion_matrix(self.labels_test,self.rf_pred_label)
        print(cm2)
        print(accuracy_score(self.labels_test,self.rf_pred_label))

    def save_random_frost(self):
        file_name = "RandomForestModel.sav"
        pickle.dump(self.RFmodel,open(file_name,'wb'))
    
    def main(self):
        print('start')
        self.make_df()
        print('df ready')
        self.train_model()
        print('train model done')
        self.save_random_frost()
        print('file is save ')
        self.check_price()


if __name__ == '__main__':
    random_forest_test = random_forest()
    random_forest_test.main()