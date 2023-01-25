from sklearn import tree
from sklearn import preprocessing
import pandas as pd

class Car_expert:
    def __init__(self,csv_file_name):
        self.csv_file = pd.read_csv(csv_file_name)
        self.inputs = []
        self.outputs = []
        self.car_brand_dic = {}
        self.car_model_dic = {}
        self.car_gear_dic = {}
        self.car_city_dic = {}
        self.car_address_dic = {}
        self.le = preprocessing.LabelEncoder()
        self.clf = tree.DecisionTreeClassifier()

    def save_le_info(self,dic_info,to_save_file_name):
        with open(f'{to_save_file_name}.txt',mode='w',encoding='utf-8') as save_file:
            save_file.write(str(dic_info))

        print(f'{to_save_file_name} / le info saved')





    def fill_dic(self,input_list, out_dic, csv_file_name, row_name):
        for index, i in enumerate(csv_file_name[row_name]):
            dic_key  =i
            if type(dic_key) == float :
                dic_key = 'None'
            out_dic[dic_key] = input_list[index]

        return out_dic

    def find_item(self,data_dic, input_string):
        out_put = 0
        for data in data_dic.items():

            if input_string == data[0]:
                out_put = data[1]

        if out_put == 0 :
            return False
        else:
            return out_put

    def fix_data(self,):
        car_brand = self.csv_file['car_brand']
        self.le.fit(car_brand)
        car_brand = self.le.transform(car_brand)
        self.car_brand_dic = self.fill_dic(car_brand, self.car_brand_dic, self.csv_file, 'car_brand')
        
        self.save_le_info(self.car_brand_dic,'car_brands')

        car_model = self.csv_file['car_model']
        self.le.fit(car_model)
        car_model = self.le.transform(car_model)
        self.car_model_dic = self.fill_dic(car_model, self.car_model_dic, self.csv_file, 'car_model')
        self.save_le_info(self.car_model_dic,'car_model')

        
        year = self.csv_file['year']
        km = self.csv_file['km']
        gear = self.csv_file['gear']
        self.le.fit(gear)
        gear = self.le.transform(gear)
        self.car_gear_dic = self.fill_dic(gear, self.car_gear_dic, self.csv_file, 'gear')
        self.save_le_info(self.car_gear_dic,'car_gear')

       
        city = self.csv_file['city']
        self.le.fit(city)
        city = self.le.transform(city)
        self.car_city_dic = self.fill_dic(city, self.car_city_dic, self.csv_file, 'city')
        self.save_le_info(self.car_city_dic,'car_city')

        address = self.csv_file['address']
        self.le.fit(address)
        address = self.le.transform(address)
        self.car_address_dic = self.fill_dic(address, self.car_address_dic, self.csv_file, 'address')
        self.save_le_info(self.car_address_dic,'car_address')

        price = self.csv_file['price']
        for index, data in enumerate(self.csv_file['id']):
            self.inputs.append([car_model[index], car_brand[index], year[index], km[index], gear[index],city[index]])
            self.outputs.append(price[index])

    def train_model(self):
        if len(self.inputs) < 3 :
            print('GET MORE CAR DATA FIRST : update DB first ! ')
        else:
            self.clf = tree.DecisionTreeClassifier()
            self.clf.fit(self.inputs,self.outputs)

    # def check_it(self,user_model,user_brand,user_year,user_gear,user_km,user_city,):
    def check_it(self):

        # TODO get input from user # get dic keys as example to show to user
        #     use to get input from user
        c = 0
        for key,value in self.car_brand_dic.items():
            if c == 3 :
                break
            else:
                print(key)
                c +=1
        
        car_input_brand = input(f'car brand : ')
        car_input_brand = self.find_item(self.car_brand_dic, car_input_brand)
        while car_input_brand == False :
            car_input_brand = input('input not valid retry .car brand : ')
            car_input_brand = self.find_item(self.car_brand_dic, car_input_brand)
        c = 0
        for key,value in self.car_model_dic.items():
            if c == 3 :
                break
            else:
                print(key)
                c +=1 

        car_input_model = input(f'car model : ')
        car_input_model = self.find_item(self.car_model_dic, car_input_model)
        while car_input_model == False :
            car_input_model = input('input not valid retry .car model : ')
            car_input_model = self.find_item(self.car_model_dic, car_input_model)
        car_input_year = int(input('year : '))
        c = 0
        for key,value in self.car_gear_dic.items():
            if c == 3 :
                break
            else:
                print(key)
                c +=1         
        car_input_gear = input('gear : ')
        car_input_gear = self.find_item(self.car_gear_dic, car_input_gear)
        while car_input_gear == False :
            car_input_gear = input('input not valid retry .car gear : ')
            car_input_gear = self.find_item(self.car_gear_dic, car_input_gear)


        car_input_km = int(input('km : '))
        c = 0
        for key,value in self.car_city_dic.items():
            if c == 3 :
                break
            else:
                print(key)
                c +=1 
        car_input_city = input('city : ')
        
        car_input_city = self.find_item(self.car_city_dic, car_input_city)
        while car_input_city == False :
            car_input_city = input('input not valid retry .car city : ')
            car_input_city = self.find_item(self.car_city_dic, car_input_city)


            # test - 01
        # user_brand = 'پژو'
        # user_model = '206'
        # user_year = 1397
        # user_gear = 'تیپ 2'
        # user_km = 67000
        # user_city = 'تهران'
        # price_of_page = numpy.str_(368000000)

            # test - 02
        # user_brand = 'پژو'
        # user_model = '206'
        # user_year = 1394
        # user_gear = 'تیپ ۳'
        # user_km = 119000
        # user_city = 'تهران'
        # price_of_page = numpy.str_(299000000)

            # test - 03
        # user_brand = 'پژو'
        # user_model = '206'
        # user_year = 1397
        # user_gear = 'تیپ ۲'
        # user_km = 93000
        # user_city = 'تهران'
        # price_of_page = numpy.str_(375000000)

            # test - 04
        # user_brand = 'کیا'
        # user_model = 'سورنتو'
        # user_year = 2017
        # user_gear = '4 سیلندر GT لاین'
        # user_km = 54700
        # user_city = 'تهران'
        # price_of_page = numpy.str_(4400000000)

            # test - 05
        # user_brand = 'دنا'
        # user_model = 'پلاس'
        # user_year = 1400
        # user_gear = 'اتوماتیک توربو'
        # user_km = 31000
        # user_city = 'تهران'
        # price_of_page = numpy.str_(616000000)

            # test - 06
        # user_brand = 'جیلی'
        # user_model = 'GC6'
        # user_year = 1398
        # user_gear = 'اکسلنت'
        # user_km = 76000
        # user_city = 'بابل'
        # price_of_page = numpy.str_(560000000)

            # test - 07
        # user_brand = 'تویوتا'
        # user_model = 'پریوس'
        # user_year = 2016
        # user_gear = 'تیپ C'
        # user_km = 63000
        # user_city = 'مشهد'
        # price_of_page = numpy.str_(1950000000)

        user_brand = self.find_item(self.car_brand_dic, car_input_brand)
        user_model = self.find_item(self.car_model_dic, car_input_model)
        user_gear = self.find_item(self.car_gear_dic, car_input_gear)
        user_city = self.find_item(self.car_city_dic, car_input_city)

        user_data = [[car_input_brand, car_input_model, car_input_year, car_input_gear, car_input_km, car_input_city]]

        answer = self.clf.predict(user_data)
        print('======= price =========')
        print(answer[0])

    def __del__(self):
        self.csv_file = None
        self.inputs = None
        self.outputs = None
        self.car_brand_dic = None
        self.car_model_dic = None
        self.car_gear_dic = None
        self.car_city_dic = None
        self.car_address_dic = None
        self.le = None
        self.clf = None


    def main(self):
        self.fix_data()
        self.train_model()
        # self.check_it()


if __name__ == '__main__':
    ml = Car_expert('auto_autoscll_page_long_break.csv')
    ml.main()