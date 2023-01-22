import os , datetime
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# TODO fix date with article date ['روز پیش','دیروز','ساعت پیش','دقیقه پیش','لحظه پیش'] . 
#  !-! time is => 01:50 am post date is for more then 2 hours ago  . store date is today but need to store yesterday date for that item 
# TODO new def find_item_with_filter([filter]); 
 
class bama_crawler:
    def __init__(self):
        self.target_url = 'https://bama.ir/car'
        self.cars_info_with_price = {}
        self.car_info_without_price = {}
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        self.cars_info_with_price_DB = 'CAR_INFO_DB_with_price'
        self.cars_info_without_price_DB = 'CAR_INFO_DB_without_price'
        # set profile to do not load images
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.driver = Firefox(executable_path='geckodriver.exe', firefox_profile=firefox_profile)
        self.driver.execute_script(f"location.href='{self.target_url}';")
        self.driver.maximize_window()
        if os.path.isfile(f'{self.cars_info_with_price_DB}.csv'):
            self.old_csv_file_with_price = pd.read_csv(f'{self.cars_info_with_price_DB}.csv')
        if os.path.isfile(f'{self.cars_info_without_price_DB}.csv'):
            self.old_csv_file_without_price = pd.read_csv(f'{self.cars_info_without_price_DB}.csv')
    def page_scroll(self,to_scroll):
        SCROLL_PAUSE_TIME = 1.5
        # TODO -NEED TO FIX- -> ISSUE 01 page body get unknown and cant scrolling || ERROR\
        #       : 'selenium.common.exceptions.JavascriptException: Message: TypeError: document.body is null'
        last_height = WebDriverWait(self.driver, 30).until(
            lambda x: x.execute_script("return document.body.scrollHeight"))
        for scroll in range(to_scroll):
            # Scroll down to bottom
            print(f'page scroll ->{scroll}/{to_scroll}' )
            sleep(3)
            # try to catch the body null error  -> execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # def check_date(self,date):
    #     # 
    #     if date == "دیروز"  :
    #         date =  datetime.date.today() - datetime.timedelta(days=1)
    #         date = date.strftime('%m%d%y')
    #         return date 
            
    #     elif "روز پیش" in date:
    #             # date.split() -> for x: if type x == int -> x= int(date[x]) - > timedelta(days=x)
    #         pass
    #     else:
    #         date = datetime.today().strftime('%m%d%y')
    #         return date 
            
    def get_page(self,  request_delay):
        scroll = int(input('enter page scroll : '))

        print(f'+page is up but , request delay -> {request_delay}s')
        sleep(request_delay)
        print(f'+ready to go ! ')
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-ad')))
            self.page_scroll(scroll)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            car_offer = soup.find_all('div', {'class': 'bama-ad-holder'})
            return car_offer
        except:
            try:
                self.driver.refresh()
                print(
                    f'-page Error reload page in -> {request_delay}s')
                sleep(request_delay)
                print(f'-ready to go ! ')
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'bama-ad')))
                self.page_scroll(scroll) # Error if page break and page scroll is false it return soup with 0 element (crawler close with no error ! )
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                car_offer = soup.find_all('div', {'class': 'bama-ad-holder'})

                return car_offer
            except:
                print('!_!_! ERROR PAGE IS BROKEN : body height is null the page is broken ')
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                car_offer = soup.find_all('div', {'class': 'bama-ad-holder'})

                return car_offer

    def save_to_csv(self, car_info, csv_file_name):
        df = pd.DataFrame.from_dict(car_info, orient='index', )
        df = df.transpose()
        if os.path.isfile(f'{csv_file_name}.csv'):df.to_csv(f'{csv_file_name}.csv',mode='a',header=False, index=0)
        else:df.to_csv(f'{csv_file_name}.csv',index=0)

    def check_point(self,out_put_file_name,car_info):
        # use to save new data .for time code can be break to do not miss new data
        with open(f'{out_put_file_name}.txt', mode='w', encoding='utf-8') as check_point:
            check_point.write(str(car_info))

    def check_page(self, car_offer):
        for car in car_offer:
            id = car.attrs['code']
            title = car.find('p', {"class": "bama-ad__title"}).text.strip()
            date = car.find('div', {'class': "bama-ad__time"}).text.strip() if car.find('div', {
                'class': "bama-ad__time"}) != None else '-1'
            car_brand = title.split('،')[0]
            car_model = title.split('،')[1]
            row_detail = car.find('div', {"class": "bama-ad__detail-row"}).find_all('span')
            year = row_detail[0].text.strip()
            km = row_detail[1].text.strip()
            km = km.replace('کیلومتر', '').replace('کارکرد صفر', '0').replace(',', '').replace('کارکرده', '-1').strip()
            gear = row_detail[2].text.strip()
            address = car.find('div', {'class': 'bama-ad__address'}).find('span').text.strip()
            city = address.split('/')[0].strip()
            location = address.split('/')[1].strip() if len(address.split('/')) > 1 else -1
            car_link = "https://bama.ir" + car.find('a').attrs['href']
            try:
                price = car.find('span', {'class': 'bama-ad__price'}).text.strip() if car.find('span', {
                    'class': 'bama-ad__price'}) != None else car.find('div',
                                                                      {'class': 'bama-ad__price-holder'}).text.strip()
            except:
                price = -1

            if price == -1 or price == 'توافقی':

                if os.path.isfile(f'{self.cars_info_without_price_DB}.csv'):
                    if id not in list(self.car_info_without_price.keys()) and id not in self.old_csv_file_without_price[
                        'id'].values:
                        self.car_info_without_price.update(
                            {id: [title, date, car_brand, car_model, year, km, gear, address, city,
                                  location, price, car_link, ]})
                    else:
                        pass
                else:
                    if id not in self.car_info_without_price.keys():
                        self.car_info_without_price.update(
                            {id: [title, date, car_brand, car_model, year, km, gear, address, city,
                                  location, price, car_link, ]})

            else:
                if os.path.isfile(f'{self.cars_info_with_price_DB}.csv'):
                    if id not in list(self.cars_info_with_price.keys()) and id not in self.old_csv_file_with_price[
                        'id'].values:
                        self.cars_info_with_price.update(
                            {id: [title, date, car_brand, car_model, year, km, gear, address, city,
                                  location, price, car_link, ]})
                    else:
                        pass
                else:
                    if id not in self.cars_info_with_price.keys():
                        self.cars_info_with_price.update(
                            {id: [title, date, car_brand, car_model, year, km, gear, address, city,
                                  location, price, car_link, ]})

        #    !_! check point is here !_!
        self.check_point('with_price',self.cars_info_with_price)
        self.check_point('without_price',self.car_info_without_price)
        print(f'+{len(self.cars_info_with_price)} cars data found')
        print(f'+{len(self.car_info_without_price)} cars data found')

    def fix_data_to_save(self, car_info, csv_filename):
        for car in list(car_info.items()):
            car_data = {
                'id': car[0],
                'title': car[1][0],
                'date': str(datetime.datetime.today()).split()[0],
                'car_brand': car[1][2],
                'car_model': car[1][3],
                'year': car[1][4],
                'km': car[1][5],
                'gear': car[1][6],
                'address': car[1][7],
                'city': car[1][8],
                'location': car[1][9],
                'price': car[1][10],
                'link': car[1][11],
            }
            self.save_to_csv(car_data, csv_filename)

    def main(self, ):
        if os.path.isfile(f'{self.cars_info_with_price_DB}.csv'):
            print(f'{len(self.old_csv_file_with_price["id"])}=< cars with price data are in DB')
        if os.path.isfile(f'{self.cars_info_without_price_DB}.csv'):
            print(f'{len(self.old_csv_file_without_price["id"])}=< cars without price data are in DB')

        print('----------- start -----------')
        page_source = self.get_page( 10)
        print(f'------page_source ready')
        self.check_page(page_source)
        print(f'------page extraction done')
        self.fix_data_to_save(self.cars_info_with_price,self.cars_info_with_price_DB)
        self.fix_data_to_save(self.car_info_without_price,self.cars_info_without_price_DB)
        print(f'---page data saved')
        self.old_csv_file_with_price = pd.read_csv(f'{self.cars_info_with_price_DB}.csv')
        self.old_csv_file_without_price = pd.read_csv(f'{self.cars_info_without_price_DB}.csv')
        print(f'{len(self.old_csv_file_with_price["id"])}=< DB size update - car with price')
        print(f'{len(self.old_csv_file_without_price["id"])}=< DB size update - car without price')
        print('----------- job done ! -----------')
        self.driver.close()

    def __del__(self):
        self.target_url = None
        self.cars_info_with_price = None
        self.header = None
        self.cars_info_with_price_DB = None


