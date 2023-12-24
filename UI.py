KV = '''
ScreenManager:
    MainScreen:
    BookingScreen:
    FormScreen:
    IDCardCheckedScreen:    
    PurchaseScreen:
    CheckinScreen:
    CheckoutScreen:
<MainScreen>
    name: "Main"
    MDScreen:
        MDRaisedButton:
            text: "Đặt phòng"
            on_release: app.booking()
            pos_hint: {'center_x':0.5,'center_y':0.6}
            #id: booking_btn   
            size_hint: .2, .16
                
        MDRaisedButton:
            text: "Trả phòng"
            on_release: app.change_scr("Checkout")
            pos_hint: {'center_x':0.5,'center_y':0.4}
            #id: checkout_btn  
            size_hint: .2, .16
    
<BookingScreen>
    name: "Booking"
    MDScreen:
        MDTopAppBar:
            elevation:1
            title:"Trang chủ"
            #left_action_items:[["menu", lambda x: app.callback(x)]]
            right_action_items:[["arrow-left" , lambda x: app.on_press_back_button()]] 
            type: 'top'
            pos_hint: {"center_x": .5,"center_y": .95}
            
        MDCard:
            id: roomone
            text: "101"
            focus_behavior: True
            orientation: "vertical"
            size_hint: None, None
            size: "280dp", "180dp"
            pos_hint: {"center_x": .25, "center_y": .65}
            padding: "8dp"
            elevation: 2
        
            on_release: app.room_chosen(self)
            
            BoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Phòng 101"
                    theme_text_color: "Secondary"
                    font_style: "H5"
                    halign: "center"
                MDLabel:
                    text: "phòng đơn"
                    theme_text_color: "Primary"
                    font_style: "Body1"
                    halign: "center" 
        
        MDCard:
            id: roomtwo
            text: "201"
            focus_behavior: True
            orientation: "vertical"
            size_hint: None, None
            size: "280dp", "180dp"
            pos_hint: {"center_x": .7, "center_y": .65}
            padding: "8dp"
            elevation: 2
            on_release: app.room_chosen(self)

            BoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Phòng 201"
                    theme_text_color: "Secondary"
                    font_style: "H5"
                    halign: "center"
                MDLabel:
                    text: "Phòng đôi"
                    theme_text_color: "Primary"
                    font_style: "Body1"
                    halign: "center"    
            
        MDCard:
            id: roomthree
            text: "102"
            focus_behavior: True
            orientation: "vertical"
            size_hint: None, None
            size: "280dp", "180dp"
            pos_hint: {"center_x": .25, "center_y": .2}
            padding: "8dp"
            elevation: 2
        
            on_release: app.room_chosen(self)
            
            BoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Phòng 102"
                    theme_text_color: "Secondary"
                    font_style: "H5"
                    halign: "center"
                MDLabel:
                    text: "phòng đơn"
                    theme_text_color: "Primary"
                    font_style: "Body1"
                    halign: "center"
            
        MDCard:
            id: roomfour
            text: "202"
            focus_behavior: True
            orientation: "vertical"
            size_hint: None, None
            size: "280dp", "180dp"
            pos_hint: {"center_x": .7, "center_y": .2}
            padding: "8dp"
            elevation: 2
        
            on_release: app.room_chosen(self)
            
            BoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Phòng 202"
                    theme_text_color: "Secondary"
                    font_style: "H5"
                    halign: "center"
                MDLabel:
                    text: "phòng đơn"
                    theme_text_color: "Primary"
                    font_style: "Body1"
                    halign: "center"              
            
<FormScreen>
    name: "Form"
    MDScreen:
        MDTopAppBar:
            elevation:1
            title:"Trang chủ"
            #left_action_items:[["menu", lambda x: app.callback(x)]]
            right_action_items:[["arrow-left" , lambda x: app.on_press_back_button()]] 
            type: 'top'
            pos_hint: {"center_x": .5,"center_y": .95}
            
        MDTextField:
            id: name_field
            hint_text: "Họ và tên: "
            size_hint_x: None
            width: "200dp"
            pos_hint: {'center_x':0.5,'center_y':0.7}
            
        MDTextField:
            id: number_field
            hint_text: "Số điện thoại"
            size_hint_x: None
            width: "200dp"
            input_filter: 'int'
            pos_hint: {'center_x':0.5,'center_y':0.6}
        
        MDTextField:
            id: email_field
            hint_text: "Địa chỉ email"
            size_hint_x: None
            width: "200dp"
            #validator: "email"
            pos_hint: {'center_x':0.5,'center_y':0.5}
            
        MDRaisedButton:
            text: "Gửi"
            on_release: app.submit(name_field.text, number_field.text, email_field.text)
            pos_hint: {'center_x':0.5,'center_y':0.4}
            id: submit_btn

<IDCardCheckedScreen>        
    name: "IDCardChecked"
    MDScreen: 
        MDTopAppBar:
            elevation:1
            title:"Trang chủ"
            #left_action_items:[["menu", lambda x: app.callback(x)]]
            right_action_items:[["arrow-left" , lambda x: app.on_press_back_button()]] 
            type: 'top'
            pos_hint: {"center_x": .5,"center_y": .95}
        Camera:
            id: camera 
            resolution: (480,480)
            play: True
        MDRaisedButton:
            text: "Chụp"
            on_release: app.capture_ID_card()
            pos_hint: {'center_x':0.5,'center_y':0.1}
            id: capture_ID_card_btn

<PurchaseScreen>
    name: "Purchase"
    MDScreen: 
        MDTopAppBar:
            elevation:1
            title:"Trang chủ"
            #left_action_items:[["menu", lambda x: app.callback(x)]]
            right_action_items:[["arrow-left" , lambda x: app.on_press_back_button()]] 
            type: 'top'
            pos_hint: {"center_x": .5,"center_y": .95}
        Image: 
            source: "QR.jpg"
    
        MDRaisedButton:
            text: "Xác nhận đã chuyển tiền"
            on_release: app.purchased()
            pos_hint: {'center_x':0.5,'center_y':0.1}

<CheckinScreen>
    name:"Checkin"
    MDScreen:
        MDTopAppBar:
            elevation:1
            title:"Trang chủ"
            #left_action_items:[["menu", lambda x: app.callback(x)]]
            right_action_items:[["arrow-left" , lambda x: app.on_press_back_button()]] 
            type: 'top'
            pos_hint: {"center_x": .5,"center_y": .95}
        MDLabel:
            text: "Xác nhận chuyển tiền thành công!"
            pos_hint: {'center_x':.7,'center_y':0.6}
            font_size: 20
                
        MDLabel:
            text: "Chúc quý khách sử dụng dịch vụ vui vẻ!"
            pos_hint: {'center_x':.7,'center_y':0.5}
            font_size: 20

<CheckoutScreen>
    name: "Checkout"
    MDScreen: 
        MDTopAppBar:
            elevation:1
            title:"Trang chủ"
            #left_action_items:[["menu", lambda x: app.callback(x)]]
            right_action_items:[["arrow-left" , lambda x: app.on_press_back_button()]] 
            type: 'top'
            pos_hint: {"center_x": .5,"center_y": .95}
        MDLabel:
            text: "Vui lòng quét thẻ phòng tại ngăn dưới để hiện room code và bấm xác nhận"
            pos_hint: {'center_x':.6,'center_y':0.8}
            font_size: 20
        
        MDTextField:
            id: room_code_field
            hint_text: "Room code: "
            size_hint_x: None
            pos_hint: {'center_x':.6,'center_y':0.7}
            input_filter: "int"
            focus: True
            max_text_length: 10
            width: "200dp"
            on_text_validate: app.checkout()
            
        MDLabel:
            id: thank_you_guest
            text: ""
            pos_hint: {'center_x':.7,'center_y':0.5}
            font_size: 20   
                                  
'''



    