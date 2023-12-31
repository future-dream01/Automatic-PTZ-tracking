# UART接收数据模块

from pyb import UART        # 导入UART模块

def biao_zhi_wei():
    # 获取标识位数组
    uart=UART(3,9600)
    a=[0,0,0,0,0,0,0,0,0]
    b=[0,0,0,0,0,0,0,0,0]
    i=0
    while(uart.any() and i<=8):
        clock.tick()
        if uart.any():
            a[i]=uart.readchar()
            i+=1
            if a[0]!=65:
                i=0
            if a[1]!=66 and i==2:
                i=0
            if i>=9:
                b=a
    return b
#print(b[2],b[3],b[4],b[5],b[6])
