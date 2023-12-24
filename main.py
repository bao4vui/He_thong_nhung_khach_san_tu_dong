
from collections.abc import Callable, Iterable, Mapping
from typing import Any
from kivy.lang import Builder
import cv2 
from kivy.uix.screenmanager import Screen,SlideTransition, ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton , MDRaisedButton
from kivy.core.window import Window
from UI import KV
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from kivy.uix.image import Image
import firebase_admin
from firebase_admin import db
import time
import threading
from kivy.clock import Clock
from rotate_servo import write_data
import numpy as np
from roboflow import Roboflow
from IDcard_detection import detect_and_crop_ID_card


class MainScreen(Screen):
    pass

class BookingScreen(Screen):
    pass 

class FormScreen(Screen):
    pass 

class IDCardCheckedScreen(Screen):
    pass 

class PurchaseScreen(Screen):
    pass

class CheckinScreen(Screen):
    pass

class CheckoutScreen(Screen):
    pass

class BackgroundTask(threading.Thread):

    def run(self):
        for i in range(3):
            print(f"Running background task {i}")
            time.sleep(1)

class BackgroundTask2(threading.Thread):
    def run(self):
        print('Nhả thẻ')
        write_data('90','0')

class BackgroundTask3(threading.Thread):
    def run(self):
        time.sleep(1)
        print('Thu hồi thẻ')
        write_data('0','180')

class BackgroundTask4(threading.Thread):
    def __init__(self,image_path):
        threading.Thread.__init__(self)
        self.image_path = image_path
    def run(self):
        print('Cắt ảnh căn cước công dân...')
        detect_and_crop_ID_card(self.image_path)


class Program(MDApp):
    
    screen_manager = ScreenManager()
    screen_manager.add_widget(MainScreen(name='Main'))
    screen_manager.add_widget(BookingScreen(name='Booking'))
    screen_manager.add_widget(FormScreen(name='Form'))
    screen_manager.add_widget(IDCardCheckedScreen(name='IDCardChecked'))
    screen_manager.add_widget(PurchaseScreen(name='Purchase'))
    screen_manager.add_widget(CheckinScreen(name='Checkin'))
    screen_manager.add_widget(CheckoutScreen(name='Checkout'))
    
    cred_obj = firebase_admin.credentials.Certificate('fir-f0bab-firebase-adminsdk-4hsv4-a7bf14b265.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL': "https://fir-f0bab-default-rtdb.firebaseio.com/"
        })
    
    rf = Roboflow(api_key="EXyCYUSm9O95EO0vkjRj")
    project = rf.workspace().project("id-card-detection-v1")
    model = project.version(1).model

    
    def build(self):
        
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.list_of_prev_screens = []
        self.ref = db.reference('/')
        
        self.myimage = Image()
        
        self.screen = Builder.load_string(KV)
              
        return self.screen
    
    def booking(self):
        '''TODO: Retreive data từ fb về lấy trạng thái phòng --> disable card''' #Done
        screen_manager = MDApp.get_running_app().root
        self.ref_room = db.reference(f'/Rooms/') 
        self.data = self.ref_room.get()
        if self.data[0]['state'] == 1:
            screen_manager.get_screen("Booking").ids.roomone.disabled = True 
        else:
            screen_manager.get_screen("Booking").ids.roomone.disabled = False     
        if self.data[1]['state'] == 1:
            screen_manager.get_screen("Booking").ids.roomthree.disabled = True  
        else:
            screen_manager.get_screen("Booking").ids.roomthree.disabled = False    
        if self.data[2]['state'] == 1:
            screen_manager.get_screen("Booking").ids.roomtwo.disabled = True  
        else:
            screen_manager.get_screen("Booking").ids.roomtwo.disabled = False    
        if self.data[3]['state'] == 1:
            screen_manager.get_screen("Booking").ids.roomfour.disabled = True  
        else:
            screen_manager.get_screen("Booking").ids.roomfour.disabled = False               
        self.list_of_prev_screens.append(self.root.current)
        self.change_scr("Booking")
    
    def fill_form(self):
        self.list_of_prev_screens.append(self.root.current)
        self.change_scr("Form")
    
    def room_chosen(self, instance):
        screen_manager = MDApp.get_running_app().root
        print(instance.text)
        self.room_id = int(instance.text)
        screen_manager.get_screen('Form').ids.name_field.text = ""
        screen_manager.get_screen('Form').ids.number_field.text = ""
        screen_manager.get_screen('Form').ids.email_field.text = ""
        self.change_scr("Form")
    
    def change_scr(self,scr):
        if scr == "Main":
            
            self.root.transition.direction = 'right'
            self.root.current = scr  
            
        if scr == "Booking" and self.root.current == 'Main':         
            self.root.transition.direction = 'left'
            self.root.current = scr 
        
        if scr == "Booking" and self.root.current == 'Form':
            self.root.transition.direction = 'right'
            self.root.current = scr 
        
        elif scr == "Form":
            
            self.list_of_prev_screens.append(self.root.current)
            self.root.transition.direction = 'left'
            self.root.current = scr   
        
        elif scr == "IDCardChecked":
            screen_manager = MDApp.get_running_app().root
            self.mycamera = screen_manager.get_screen("IDCardChecked").ids.camera
            self.mycamera.play = True
            if self.root.current == 'Booking':   
                self.root.transition.direction = 'left'
                
            else: 
                self.root.transition.direction = 'right'
            self.root.current = scr     
        
        elif scr == "Purchase":
            if self.root.current == 'IDCardChecked':   
                self.root.transition.direction = 'left'
                
            else: 
                self.root.transition.direction = 'right'
            self.root.current = scr
        
        elif scr == "Checkin":
            self.root.transition.direction = 'left'
            self.root.current = scr   
             
        
        elif scr == "Checkout":
            self.background_task2 = BackgroundTask2()
            self.background_task2.start()
            Clock.schedule_interval(self.check_thread2, 1) 
               
            screen_manager = MDApp.get_running_app().root
            self.root.transition.direction = 'left'
            self.root.current = scr
            screen_manager.get_screen('Checkout').ids.room_code_field.focus = True
            
            
         
    def submit(self,name, number, email):
        '''TODO: Cập nhật data vào firebase''' ##Done
        self.ref = db.reference('/Customers')
        self.ref.update({
            f'{len(self.ref.get())}': 
            {
                "customerID": len(self.ref.get()),
                "email": email,
                "isPurchased": False,
                "isUsing": 0 ,
                "name": name,
                "phonenumber": number,
                "roomID": self.room_id
            }
        })
        self.list_of_prev_screens.append(self.root.current)
        self.change_scr("IDCardChecked")
        pass    
    
    def capture_ID_card(self):
        screen_manager = MDApp.get_running_app().root
        self.mycamera = screen_manager.get_screen("IDCardChecked").ids.camera  
        self.myimage = Image()
        timenow = time.strftime("%Y%m%d_%H%M%S")
        self.mycamera.export_to_png("myimage_{}.png".format(timenow))
        self.myimage.source = "myimage_{}.png".format(timenow)
        self.mycamera.play = False  
        '''TODO: Cắt ảnh căn cước công dân'''  
        self.background_task4 = BackgroundTask4(self.myimage.source)
        self.background_task4.start()
        Clock.schedule_interval(self.check_thread4, 3) 
        self.change_scr("Purchase") 
    
    def purchased(self):
        '''TODO: Kiểm tra trạng thái thanh toán
                Bắt chờ trong 10s, thành công thì chuyển màn, không thì nhảy thông báo chưa thành công #Done
                 Set up chay trạng thái thanh toán trên fb là true -> chuyển màn, Servo quay nhả thẻ    #Done
                 '''
         
        # print(self.ref_room.get())
        # print(self.ref_room.child('0').get())
        self.ref.child(f'{len(self.ref.get())-1}').update({"isPurchased": True, 
                                                         "isUsing": 1})   
        iter = 0  
        room = False 
        for dict in self.ref_room.get():

            for key, value in dict.items():
                if key == 'roomID' and value == self.room_id:
                    self.ref_room.child(str(iter)).update({"state": 1})
                    room = True
                    break 
            if room == True: break    
            iter += 1 
        self.background_task2 = BackgroundTask2()
        self.background_task2.start()
        Clock.schedule_interval(self.check_thread2, 1) 
               
        self.change_scr("Checkin")
        
        self.background_task3 = BackgroundTask3()
        self.background_task3.start()
        Clock.schedule_interval(self.check_thread3, 1) 
    
    def on_press_back_button(self):
        if self.root.current == 'Checkin':
            self.list_of_prev_screens.clear()
            self.change_scr("Main")
            
        elif len(self.list_of_prev_screens) > 0:
            #
            print(self.list_of_prev_screens)
            self.change_scr(self.list_of_prev_screens[-1])
            self.list_of_prev_screens.pop()
    
    def checkout(self):
        screen_manager = MDApp.get_running_app().root
        self.ref = db.reference('/Customers/')
        self.ref_room = db.reference(f'/Rooms/') 
        current_customers = len(self.ref.get())
        self.roomcode = screen_manager.get_screen('Checkout').ids.room_code_field.text
        
        if len(self.roomcode) >= 10: 
            '''TODO: '''   #Done
            #làm thêm một vài logic cạp nhật database trong đây nữa (100%) 
            print(current_customers)
            iter = 0  
            iter_cus = 0
            room = False 
            for dict in self.ref_room.get():
                #print(self.ref_room.child(str(iter)).get())
                for key, value in dict.items():
                    if key == 'roomcode' and str(value) == str(self.roomcode):
                        self.ref_room.child(str(iter)).update({"state": 0})
                        room = True
  
                if room == True: break        
                else: iter += 1         
                
            for dict_customer in self.ref.get():
                for key2, value2 in dict_customer.items():
                    try:
                        if key2 == 'roomID' and value2 == self.ref.child(str(iter)).get()['roomID']:
                            self.ref.child(str(iter_cus)).update({"isUsing": 0}) 
                            break
                    except: break    
                iter_cus += 1
                if iter_cus == current_customers: break
                  
            screen_manager.get_screen('Checkout').ids.thank_you_guest.text =  "Cảm ơn quý khách đã đặt phòng và sử dụng dịch vụ, hẹn gặp lại!"
            
        self.background_task = BackgroundTask()
        self.background_task.start()
        Clock.schedule_interval(self.check_thread, 0.1)
        
        self.background_task3 = BackgroundTask3()
        self.background_task3.start()
        Clock.schedule_interval(self.check_thread3, 1) 
        
    def check_thread(self, dt):
        screen_manager = MDApp.get_running_app().root
        
        if not self.background_task.is_alive():       
            self.change_scr("Main")
            Clock.unschedule(self.check_thread)
            screen_manager.get_screen('Checkout').ids.thank_you_guest.text =  ""    
    
    def check_thread2(self, dt):
        
        if not self.background_task2.is_alive():       
            #self.change_scr("Main")
            Clock.unschedule(self.check_thread2)        
    
    def check_thread3(self, dt):
        
        if not self.background_task3.is_alive():       
            #self.change_scr("Main")
            Clock.unschedule(self.check_thread3)   
    
    def check_thread4(self, dt):
        
        if not self.background_task4.is_alive():       
            #self.change_scr("Main")
            Clock.unschedule(self.check_thread4)   
        
Program().run()    