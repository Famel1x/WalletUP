from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.floatlayout import FloatLayout
import json
from kivymd.uix.list import MDList, ThreeLineListItem
from kivymd.uix.textfield import MDTextField
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.config import Config
from kivy.core.window import Window
import cv2
from pyzbar.pyzbar import decode
import re
import requests

screen_helper = """
ScreenManager:
    WelcomeScreen:
    HomeScreen:
    HistoryScreen:
    BolsheScreen:
<WelcomeScreen>:
    name: 'Welcome'
    MDLabel:
        text: 'WalletUp'
        pos_hint: {'center_x':0.92,'center_y':0.8}
    MDFillRoundFlatButton:
        text: 'Войти в приложение'
        pos_hint: {'center_x':0.5,'center_y':0.6}
        on_press: root.manager.current = 'home'
    MDFillRoundFlatButton:
        text: 'Выход'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        on_press: app.stop()
        
    MDFillRoundFlatButton:
        text: 'Сменить тему'
        pos_hint: {'center_x' : 0.5, 'center_y':0.2}
        on_press: app.theme()






<HomeScreen>:
    name: 'home'
    id: Homescreen
    MDLabel:
        text: 'Главная'
        pos_hint :{'center_y': 0.95, 'center_x': 0.55}
        
    MDLabel:
        text: 'Баланс: '
        pos_hint :{'center_y': 0.80, 'center_x': 0.55}
        
    
        

    MDTextField:
        hint_text: "Введите итог"
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint_x: .3
        id: entry
        focus: True 

    MDTextField:
        hint_text: "Назввание"
        pos_hint: {"center_x": .5, "center_y": .7}
        size_hint_x: .3
        id: name
        focus: True 
    
    MDFillRoundFlatButton:
        text:'+'
        pos_hint :{'center_y': 0.5, 'center_x': 0.8}
        on_release: app.reviveBalance(entry.text, 1, name.text)
        on_press: balan.text = app.balance  + " ₽"
        
    MDFillRoundFlatButton:
        text: "Обновить"
        pos_hint: {"center_x": .85, "center_y": .95}
        on_release: balan.text = app.balance + " ₽"
    
    MDFillRoundFlatButton:
        text:'-'
        pos_hint :{'center_y': 0.5, 'center_x': 0.2}
        on_release: app.reviveBalance(entry.text, 0, name.text)
        on_press: balan.text = app.balance + " ₽"
    
    MDLabel:
        id: balan
        text: app.balance
        pos_hint:{'center_y':0.8, 'center_x': 0.8}
    
    
    
    MDFillRoundFlatButton:
        text:'Главная'
        pos_hint :{'center_y': 0.05, 'center_x': 0.13}
        on_press: root.manager.current = 'Welcome'      
    MDFillRoundFlatButton:
        text:'История '
        pos_hint :{'center_y': 0.05, 'center_x': 0.4}
        on_press: root.manager.current = 'history'  
    MDFillRoundFlatButton:
        text:'QR'
        pos_hint :{'center_y': 0.05, 'center_x': 0.64}
        on_release: app.request()
    MDFillRoundFlatButton:
        text:'Больше'
        pos_hint :{'center_y': 0.05, 'center_x': 0.87}
        on_press:root.manager.current = 'bolshe'




<HistoryScreen>:
    name: 'history'
    

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True
    
        Label:
            size_hint_y: None
            height: self.texture_size[1]
            text_size: 150, None
            id:his
            text: app.data
        
    MDFillRoundFlatButton:
        text: 'Назад'
        pos_hint: {'center_x':0.12,'center_y':0.95}
        on_press: root.manager.current = 'home'
        
    MDFillRoundFlatButton:
        text: 'Обновить'
        pos_hint: {'center_x':0.85,'center_y':0.95}
        on_press: his.text = app.data




<BolsheScreen>:
    name: 'bolshe'
    
    MDLabel: 
        text: 'Резервация средств: '
        pos_hint:{'center_y':0.95, 'center_x': 0.55}
    
    MDLabel: 
        text: app.uzerezerv
        pos_hint:{'center_y':0.9, 'center_x': 0.55}
     
    MDFillRoundFlatButton:
        text: 'Зарезервировать'
        pos_hint: {'center_x':0.51,'center_y':0.77}
        on_press: app.rezrevirovanie(wall.text)
    
    MDTextField:
        hint_text: "Сумма резервации"
        pos_hint: {"center_x": .5, "center_y": .83}
        size_hint_x: .3
        id: wall
        focus: True  
    
    MDFillRoundFlatButton:
        text: 'Назад'
        pos_hint: {'center_x':0.12,'center_y':0.05}
        on_press: root.manager.current = 'home'


"""


class WelcomeScreen(Screen):
    pass



class HomeScreen(Screen):
    pass


class HistoryScreen(Screen):
    pass

class BolsheScreen(Screen):
    pass

class analizScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='Welcome'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(HistoryScreen(name='history'))
sm.add_widget(BolsheScreen(name ='bolshe'))
sm.add_widget(analizScreen(name ='analiz'))


class DemoApp(MDApp):


    def build(self):

        Window.size = (360, 800)
        self.uzerezerv = ")"
        self.data = 0
        self.score = 0
        default = {"score": 0}

        try:
            with open("data.txt") as data:
                l = json.load(data)
                self.score = l["score"]
        except:
            with open("data.txt", "w") as data:
                json.dump(default, data)

            with open("data.txt") as data:
                l = json.load(data)
                self.score = l["score"]

        self.rezerv = 0
        default = {"score": 0}

        try:
            with open("rezerv.txt") as data:
                l = json.load(data)
                self.rezerv = l["score"]
        except:
            with open("rezerv.txt", "w") as data:
                json.dump(default, data)

            with open("rezerv.txt") as data:
                l = json.load(data)
                self.rezerv = l["score"]

        self.uzerezerv = ("Уже зарезервировано: " + str(self.rezerv))

        self.historyload()

        with open("config.txt", "r") as f:
            theme_of_file = f.read().split(' ')

        self.theme_cls.primary_palette = theme_of_file[1]
        self.theme_cls.theme_style = theme_of_file[0]
        self.balance = str(self.score)
        self.balance = self.balance + " ₽"



        screen = Builder.load_string(screen_helper)

        return screen




    def reading_qrcode(self):
        while True: # Ищет  qr-код, пока не найдёт
            capture = cv2.VideoCapture(0) # Подключение к камере номер 0, вебка по умолчанию
            rez, img = capture.read()
            if rez == False: # Проверка наличия камеры
                return "error: cam not found"
            decoded = decode(img)
            if len(decoded) == 0:
                print( "Поиск QR-кода")
            else:
                string_of_data: str = decoded[0].data.decode("utf-8")

                if re.search('t=', string_of_data) == None or re.search('s=', string_of_data) == None or re.search('fn=', string_of_data) == None or re.search('i=', string_of_data) == None or re.search('fp=', string_of_data) == None or re.search('n=', string_of_data) == None:
                    return 'error: invalid pattern qrcode'

                value = string_of_data.split('&')
                datetime = value[0][2:len(value[0])]

                year = datetime[0:4]
                month = datetime[4:6]
                day = datetime[6:8]
                hours = datetime[9:11]
                minutes = datetime[11:13]
                seconds = datetime[13:15]

                check_amount = round(float(value[1][2:len(value[1])]), 2)
                fn: str = value[2][3:len(value[2])]
                fd = value[3][2:len(value[3])]
                fp: str = value[4][3:len(value[4])]
                n_of_value = value[5][2:len(value[5])]
                #return year, month, day, hours, minutes, seconds, check_amount, fn, fd, fp, n_of_value, string_of_data
                return {'year': year, 'month': month, 'day': day, 'hours': hours, 'minutes': minutes, 'seconds': seconds, 'check_amount': check_amount, 'fn': fn, 'fd': fd, 'fp': fp, 'n_of_value': n_of_value, 'string_of_data': string_of_data}
                
    #Функция запроса на сайт, принимает строку с сухими данными из qr-кода, возвращает словарь
    def request(self):
        url = 'https://proverkacheka.com/api/v1/check/get'
        qr_code = self.reading_qrcode()
        
        if qr_code == "error: cam not found" or qr_code == "error: invalid pattern qrcode":
            print("critical error")
            return 
            
        
        data={'token': '20570.IFPlTS1sxFJ3Jsvfr','qrraw': qr_code['string_of_data']}
        result_data = json.loads(requests.post(url, data=data).text)
        if result_data["code"] == 1:
            self.reviveBalance((qr_code['check_amount']), 0, result_data["data"]["json"]["retailPlace"] + ' ' + result_data["data"]["json"]["user"])

            self.dialog = MDDialog(
                    text="Чек добавлен в историю",size_hint = (0.5,1),
                    buttons=[
                        MDFlatButton(
                            text="Окей", text_color=self.theme_cls.primary_color, on_press = self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()
        else:
            print("Error: check request is False")




    def reviveBalance(self, dans, mean, name):
        a = int(dans)

        if mean == 1:
            self.score += a
            self.balance  = str(self.score)
            db = {"score": self.score}
            with open("data.txt", "w") as data:
                json.dump(db, data)

            self.historyadd("Пополнение", name, dans,self.balance)


        else:
            if (self.score - a) < self.rezerv:
                self.dialog = MDDialog(
                    text="Нельзя потратить больше чем вы зарезервировали",size_hint = (0.5,1),
                    buttons=[
                        MDFlatButton(
                            text="Окей", text_color=self.theme_cls.primary_color, on_press = self.close_dialog
                        ),
                    ],
                )
                self.dialog.open()
            else:
                self.score -= a
                self.balance = str(self.score)
                db = {"score": self.score}
                with open("data.txt", "w") as data:
                    json.dump(db, data)

                self.historyadd("Расход", name, dans, self.balance)

    # 1. Name - summ (oboznach)
    def close_dialog(self, obj):
        self.dialog.dismiss()

    def historyadd(self, status, name, count, ostatok):

        hist = ('Название: ',name,'\nСтатус: ',status,'\nСумма: ',count,'\nОстаток: ', ostatok,'\n ','\n')
        histr=("%s%s%s%s%s%s%s%s%s%s")%(hist)
        print(histr)

        file = open("history.txt", "a")
        file.write(histr)
        file.close()
        self.historyload()

    def historyload(self):
        file = open("history.txt", "r")
        self.data = file.read()
        print(self.data)

    def rezrevirovanie(self, deam):
        self.a = int(deam)
        db = {"score": self.a}
        with open("rezerv.txt", "w") as data:
            json.dump(db, data)
        self.dialog = MDDialog(
                    text="Для применения настроек, перезапустите приложение",size_hint = (0.5,1),
                    buttons=[
                        MDFlatButton(
                            text="Окей", text_color=self.theme_cls.primary_color, on_press = self.close_dialog
                        ),
                    ],
                )
        self.dialog.open()

    def theme(self):
        with open("config.txt", "w") as f:
            if self.theme_cls.theme_style == "Light":
                f.write("Dark Yellow")
            else:
                f.write("Light Blue")

            self.dialog = MDDialog(
                    text="Для применения настроек темы, перезапустите приложение",size_hint = (0.5,1),
                    buttons=[
                        MDFlatButton(
                            text="Окей", text_color=self.theme_cls.primary_color, on_press = self.close_dialog
                        ),
                    ],
                )
            self.dialog.open()








DemoApp().run()