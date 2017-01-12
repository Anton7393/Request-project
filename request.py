import requests

class Requester:
    def __init__(self):
        self.input_data()

    def input_data(self):
        print("Введите название зоны. Пример: Europe, Asia etc")
        self.location = str(input())
        print("Ведите название города. Пример: Moscow, Chicago etc")
        self.s_city = str(input())
        self.full_location = self.location + '/' + self.s_city
        self.time_request(self.full_location)

    def switcher(self):
        print("Y/N")
        x = str(input())
        if x == "Y":
            self.id_request(self.s_city)
        elif x == "N":
            print("Попробуйте ещё раз")
            self.input_data()
        else:
            self.switcher()

    def time_request(self, full_location):
        self.apikey = "LRDY5VUKWTYX"

        try:
            res = requests.get("http://api.timezonedb.com/v2/get-time-zone",
                               params={'key': self.apikey, 'zone': full_location, 'format': 'json', 'by': 'zone'})
            time = res.json()
            if time['status'] == "OK":
                print("Time: ", time["formatted"])
                self.id_request(self.s_city)
            elif time['status'] != "OK":
                print("Ошибка ввода координат")
                print("В случае продолжения - пользователь рискует получить не верные данные")
                print('Хотите продолжить?')
                self.switcher()
        except Exception as e:
            print("Exception (request):", e)
            pass

    def id_request(self, s_city):
        self.city_id = 0
        self.appid = "a286392a840dc328b0617b6002d2e206"
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': self.appid})
            data = res.json()
            if data['count'] > 0:
                cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
                self.city_id = data['list'][0]['id']

            self.weather_request(self)
        except Exception as e:
            print("Exception (find):", e)
            pass

    def weather_request(self, city_id):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': self.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': self.appid})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            print("temp:", data['main']['temp'])
            print("temp_min:", data['main']['temp_min'])
            print("temp_max:", data['main']['temp_max'])
        except Exception as e:
            print("Exception (weather):", e)
            pass

One = Requester()