# 舵机复位模块
from pyb import Servo,LED                                # 从pyb模块引入Servo类
from shuju import biao_zhi_wei
import pyb

led1=LED(1)
led2=LED(2)
s1=Servo(1)                                          # 初始化舵机1
s2=Servo(2)                                          # 初始化舵机2
angle0=[]
#######################################################################################################################################
def hui_zhongdian():
    # 舵机复位函数
    s1.angle(angle0[0])
    s2.angle(angle0[1])
#######################################################################################################################################
def jiaozhun():
    # 矫准函数
    while(True):
        led1.on()
        led2.off()
        b=biao_zhi_wei()
        if b==[65,66,0,0,0,0,0,0,1]:
            angle0.append(s1.angle())
            angle0.append(s2.angle())
            led2.on()
            led1.off()
            pyb.delay(500)
        if len(angle0)==10:
            break
    return angle0

