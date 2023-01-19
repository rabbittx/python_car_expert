import pandas as pd
from sklearn import  preprocessing
import os ,datetime

#TODO change it to class
    # fix data for random frost csv file class
#TODO save car dics to can get input from user
    # to check user input string with it number value



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

with_price = pd.read_csv("CAR_INFO_DB_with_price.csv")
without_price = pd.read_csv("CAR_INFO_DB_without_price.csv")

le = preprocessing.LabelEncoder()


new_date = with_price['date']
new_date_list = []
for date_time in new_date :

    if len(date_time.split('-')) < 3 :
        new_date_time =  str(datetime.datetime.today()).split()[0]
    else: new_date_time = date_time
    new_date_time = new_date_time.split('-')

    new_date_time = new_date_time[0] + new_date_time[1] + new_date_time[2]
    print(new_date_time)
    new_date_list.append(int(new_date_time))

car_brand = with_price['car_brand']
le.fit(car_brand)
car_brand = le.transform(car_brand)
car_brand_dic = fill_dic(car_brand, car_brand_dic, with_price, 'car_brand')
car_model = with_price['car_model']
le.fit(car_model)
car_model = le.transform(car_model)
car_model_dic = fill_dic(car_model, car_model_dic, with_price, 'car_model')
year = with_price['year']
km = with_price['km']
gear = with_price['gear']
le.fit(gear)
gear = le.transform(gear)
car_gear_dic = fill_dic(gear, car_gear_dic, with_price, 'gear')
city = with_price['city']
le.fit(city)
city = le.transform(city)
car_city_dic = fill_dic(city, car_city_dic, with_price, 'city')
address = with_price['address']
le.fit(address)
address = le.transform(address)
car_address_dic = fill_dic(address, car_address_dic, with_price, 'address')
price = with_price['price']

mydic = {}
for index, data in enumerate(with_price['id']):
    mydic[data] =[car_brand[index] ,car_model[index], year[index], km[index], gear[index], city[index],price[index],new_date_list[index]]



    car_data = {
        'id': data,
        'date': new_date_list[index],
        'car_brand': car_brand[index],
        'car_model': car_model[index],
        'year': year[index],
        'km': km[index],
        'gear': gear[index],
        'city': city[index],
        'price': price[index],

    }
    save_to_csv(car_data, 'to_use_for_random_frost_without_price')



class data_fixer:
    def __init__(self):
        pass

    def fill_dic(self):
        pass
    
    def save_to_csv(self):
        pass
    
    def fix_data(self):
        pass
    
    def __del__(self):
        pass