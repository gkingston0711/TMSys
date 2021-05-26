##################################
# MLX90640 Test with Raspberry Pi
##################################
#

import time,board,busio
import numpy as np
import adafruit_mlx90640
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date



def takeTemp():

    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
    mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate

    frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
    while True:
        try:
            mlx.getFrame(frame) # read MLX temperatures into frame var
            break
        except ValueError:
            continue # if error, just read again

    return (((9.0/5.0)*np.mean(frame))+32.00)

def addTemp(array,temp,Size):

    s=len(array)

    if(s>=Size):
        array.pop(0)
        array.append(temp)
    else:
        array.append(temp)

def slidingWindow(array,Size):
    
    n=len(array)
    average=0

    if n<Size:
        print("sample size to small, wait till larger")
        return average

    #first ave

    for num in array:
        average+=num

    average=average/Size

    return average

def tempCompare(todayTemp,aveTemp,var,array):

    L=len(array)

    if todayTemp >= aveTemp+var and L==5:
        print("your temp today is higher then normal, please check your tempurature more accuatly and advice with a physician")
        
        send_message()

    if todayTemp<= aveTemp-var and L==5:
        print("Your temp today is to low, please check on a more accureate device then consulte with your physician")
        
        send_message()


def send_message():

    email_user = 'kingston@pdx.edu'
    email_password = 'Chester67'
    email_send = 'kingston@pdx.edu'
    subject = 'Body Temps'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject


    body = 'This email contains sensative information: body temps'
    msg.attach(MIMEText(body,'plain'))

    filename='temp_history.txt'
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()

def main():

    temps=[]
    Size=5
    Var=3

    #Infinate loop
    while(True):

        val=takeTemp()
        val=round(val)
        addTemp(temps,val,Size)
    
        file_object=open("temp_history.txt","a")
        str_temp=str(val)+" for date "+str(date.today())+" *** "

        file_object.write(str_temp)

        time.sleep(2)

        ave=slidingWindow(temps,Size)

        if ave >1:
            print(ave)

        tempCompare(val,ave,Var,temps)

        file_object.close()

main()
