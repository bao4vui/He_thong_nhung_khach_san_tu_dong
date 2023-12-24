import serial
import time

arduino = serial.Serial(port = 'COM3', baudrate = 9600, timeout=1)

def write_data(servo_value,servo_value2):
    #global servo_value ,angles
    while True:
        # delim = bytes(';', "utf-8")
        # angles = ( bytes(str(int(servo_value)), "utf-8"))

        # arduino.write(bytes(str(int(servo_value)), "utf-8"))    
        # arduino.write(delim)
        #servo_value = input('Number')
        time.sleep(3)
        arduino.write(servo_value.encode())
        # print(servo_value.encode())
        time.sleep(5)
        arduino.write(servo_value2.encode())
        time.sleep(2)
        break


#write_data('90','180')