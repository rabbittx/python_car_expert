from fetch_data import bama_crawler
from tree import Car_expert
import pickle

class Panel(bama_crawler ,Car_expert,):
    def __init__(self, page_scroll_num, csv_file_name):
        self.crawler_page_scroll = page_scroll_num
        self.car_info_CSV_file_name = csv_file_name
        self.car_expert = None
        self.bama_crawler = None
        self.panel_ans = 0

    def update_DB(self):
        print('Panel : start to update DB')
        if self.bama_crawler == None:
            self.bama_crawler = bama_crawler()
            self.bama_crawler.main(self.crawler_page_scroll)
        else:
            self.bama_crawler.main(self.crawler_page_scroll)
        print('Panel : DB update done ')

    def train_car_expert(self):
        print('Panel : car export start')
        self.car_expert = Car_expert(self.car_info_CSV_file_name)
        self.car_expert.fix_data()
        print('Panel : car export start to train model')
        self.car_expert.train_model()
        print('Panel : car export model is ready')

    def check_car_price(self):
        # remove input from here and get them from user inside of function
        user_brand = 'جیلی'
        user_model = 'GC6'
        user_year = 1398
        user_gear = 'اکسلنت'
        user_km = 76000
        user_city = 'بابل'
        self.car_expert.check_it(user_brand,user_model,user_year,user_gear,user_km,user_city,)

    def panel_menu(self):

        while self.panel_ans != -1:
            print('----------- car info panel ------------')
            print('1. update the DB')
            print('2. train car expert')
            print('3. check your car price ')
            # print('4. random forest ')

            print('-1 to close panel ')
            self.panel_ans = int(input('enter 1 , 2 , 3 or -1 : '))

            while type(self.panel_ans) != int:
                print(type(self.panel_ans))
                self.panel_ans = int(input('enter 1 , 2 , 3 or -1 :'))

            if self.panel_ans == 1:
                self.update_DB()
                self.panel_menu()
            elif self.panel_ans == 2:
                self.train_car_expert()
                self.panel_menu()

            elif self.panel_ans == 3:
                if self.car_expert == None:
                    print('need to train car expert first !')
                    self.panel_menu()
                else:
                    self.check_car_price()
                    self.panel_menu()

                # TODO   need more data to use this part : (3794/5521):0.581857219538379
            # elif self.panel_ans == 4 :
            #     RFmodel = pickle.load(open('RandomForestModel.sav', 'rb'))
            #     [user_brand,user_model,user_year,user_gear,user_km,user_city,]
            #     predicted_value = RFmodel.predict(data)


    def __del__(self):
        self.crawler_page_scroll = None
        self.car_info_CSV_file_name = None
        self.car_expert = None
        self.bama_crawler = None
        self.panel_ans = None

if __name__ == '__main__':
    page_scroll = 100
    csv_file = 'CAR_INFO_DB_with_price.csv'
    panel = Panel(page_scroll,csv_file)
    panel.panel_menu()
