import pandas as pd
from sklearn import  preprocessing
import os ,datetime

#TODO change it to class
    # fix data for random forest csv file class
#TODO save car dics to can get input from user
    # to check user input string with it number value



# def fill_dic(input_list, out_dic, csv_file_name, row_name):
#     for index, i in enumerate(csv_file_name[row_name]):
#         dic_key = i
#         if type(dic_key) == float:
#             dic_key = f'None{index}'

#         out_dic[dic_key] = input_list[index]

#     return out_dic


# def save_to_csv(car_info, csv_file_name):
#         df = pd.DataFrame.from_dict(car_info, orient='index', )
#         df = df.transpose()
#         if os.path.isfile(f'{csv_file_name}.csv'):df.to_csv(f'{csv_file_name}.csv',mode='a',header=False, index=0)
#         else:df.to_csv(f'{csv_file_name}.csv',index=0)


# car_brand_dic = {}
# car_model_dic = {}
# car_gear_dic = {}
# car_city_dic = {}
# car_address_dic = {}
# car_date_dic = {}

# with_price = pd.read_csv("CAR_INFO_DB_with_price.csv")
# without_price = pd.read_csv("CAR_INFO_DB_without_price.csv")

# le = preprocessing.LabelEncoder()


# new_date = with_price['date']
# new_date_list = []
# for date_time in new_date :

#     if len(date_time.split('-')) < 3 :
#         new_date_time =  str(datetime.datetime.today()).split()[0]
#     else: new_date_time = date_time
#     new_date_time = new_date_time.split('-')

#     new_date_time = new_date_time[0] + new_date_time[1] + new_date_time[2]
#     print(new_date_time)
#     new_date_list.append(int(new_date_time))

# car_brand = with_price['car_brand']
# le.fit(car_brand)
# car_brand = le.transform(car_brand)
# car_brand_dic = fill_dic(car_brand, car_brand_dic, with_price, 'car_brand')
# car_model = with_price['car_model']
# le.fit(car_model)
# car_model = le.transform(car_model)
# car_model_dic = fill_dic(car_model, car_model_dic, with_price, 'car_model')
# year = with_price['year']
# km = with_price['km']
# gear = with_price['gear']
# le.fit(gear)
# gear = le.transform(gear)
# car_gear_dic = fill_dic(gear, car_gear_dic, with_price, 'gear')
# city = with_price['city']
# le.fit(city)
# city = le.transform(city)
# car_city_dic = fill_dic(city, car_city_dic, with_price, 'city')
# address = with_price['address']
# le.fit(address)
# address = le.transform(address)
# car_address_dic = fill_dic(address, car_address_dic, with_price, 'address')
# price = with_price['price']

# mydic = {}
# for index, data in enumerate(with_price['id']):
#     mydic[data] =[car_brand[index] ,car_model[index], year[index], km[index], gear[index], city[index],price[index],new_date_list[index]]



#     car_data = {
#         'id': data,
#         'date': new_date_list[index],
#         'car_brand': car_brand[index],
#         'car_model': car_model[index],
#         'year': year[index],
#         'km': km[index],
#         'gear': gear[index],
#         'city': city[index],
#         'price': price[index],

#     }
#     save_to_csv(car_data, 'to_use_for_random_forest_without_price')



class data_fixer:
    def __init__(self):
        self.car_brand = []
        self.car_model = []
        self.car_gear = []
        self.car_city = []
        self.car_address = []
        self.car_date = []
        self.car_price = []
        self.date_list = []
        self.with_price = pd.read_csv("CAR_INFO_DB_with_price.csv")
        self.without_price = pd.read_csv("CAR_INFO_DB_without_price.csv")
        self.le = preprocessing.LabelEncoder()


    def fill_dic(self,csv_file,out_dic,input_list,row_name):
        for index, i in enumerate(csv_file[row_name]):
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

    def lables_data(self,csv_title_string,csv_file):    
        csv_title_string = 'date'
        if csv_title_string == 'date':    
            new_date = with_price['date']
            for date_time in new_date :
                new_date_time = new_date_time.split('-')
                new_date_time = new_date_time[0] + new_date_time[1] + new_date_time[2]
                self.new_date_list.append(int(new_date_time))
            return self.new_date_list
        elif csv_title_string == 'km':
            column_data = with_price['km']
            return column_data
        elif csv_title_string == 'price':
            column_data = with_price['price']
            return column_data
        elif csv_title_string =='year':    
            column_data = with_price['year']
            return column_data
        else:
            column_data = csv_file[csv_title_string]
            self.le.fit(column_data)
            column_data = self.le.transform(column_data)
            output_dic = self.fill_dic(column_data, output_dic, csv_file, csv_title_string)
            return [output_dic , column_data]
    
    def fix_data_save(self,car_brand,car_model,year,km,gear,city,price,new_date_list,csv_file,output_csv_file_name_string):
        for index, data in enumerate(csv_file['id']):
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
            self.save_to_csv(car_data, output_csv_file_name)
    def fix_with_price_data(self):
        print('start with')
        self.car_brand = self.lables_data('car_brand',self.with_price)
        self.car_model = self.lables_data('car_model',self.with_price)
        self.year = self.lables_data('year',self.with_price)
        self.km = self.lables_data('km',self.with_price)
        self.gear = self.lables_data('gear',self.with_price)
        self.city = self.lables_data('city',self.with_price)
        self.date_list = self.lables_data('date',self.with_price)
        self.car_price = self.lables_data('price',self.with_price)
        self.fix_data_save(self,car_brand[1],car_model[1],year,km,gear[1],city[1],car_price,date_list,self.with_price,'random_forest_data_with_price')
        print('done with')

    def fix_with_price_data(self):
        print('start without')
        self.car_brand = self.lables_data('car_brand',self.without_price)
        self.car_model = self.lables_data('car_model',self.without_price)
        self.year = self.lables_data('year',self.without_price)
        self.km = self.lables_data('km',self.without_price)
        self.gear = self.lables_data('gear',self.without_price)
        self.city = self.lables_data('city',self.without_price)
        self.date_list = self.lables_data('date',self.without_price)
        self.car_price = self.lables_data('price',self.without_price)
        self.fix_data_save(self,car_brand[1],car_model[1],year,km,gear[1],city[1],car_price,date_list,self.without_price,'random_forest_data_without_price')
        print('done without')

    def main(self):
        print('start')
        self.fix_with_price_data()
        self.fix_without_price_data()
        print('end')



    def __del__(self):
        self.car_brand_dic = None
        self.car_model_dic = None
        self.car_gear_dic = None
        self.car_city_dic = None
        self.car_address_dic = None
        self.car_date_dic = None
        self.new_date_list = None
        self.with_price = None
        self.without_price = None
        self.le = None

if __name__ == '__main__':
    data_fixer = data_fixer()
    data_fixer.main()