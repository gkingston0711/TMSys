##################################
# MLX90640 Test with Raspberry Pi
##################################
#
import time,board,busio
import numpy as np
import adafruit_mlx90640
import time


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

    # print out the average temperature from the MLX90640
    #print('Average MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.\
    #      format(np.mean(frame),(((9.0/5.0)*np.mean(frame))+32.0)))

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

    if todayTemp<= aveTemp-var and L==5:
        print("Your temp today is to low, please check on a more accureate device then consulte with your physician")
        
def main():
    temps=[]
    Size=5
    Var=3
    
    #forever loop
    while(True):
        val=takeTemp()
        val=round(val)
        addTemp(temps,val,Size)
        time.sleep(3)
        
        ave=slidingWindow(temps,Size)

        if ave >1:
            print(ave)

        tempCompare(val,ave,Var,temps)



main()
