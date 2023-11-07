import sensor, image, time, math,time,lcd ,pyb       # 导入函数所依赖的模块：传感器、图像、定时器模块、数学函数模块(python标准库)、时间模块(追踪运行时间)
from pid import Pid                                  # 从pid模块导入Pid类
from pyb import Servo,UART                           # 从pyb模块引入Servo类
from shuju import biao_zhi_wei                       # 从shuju模块导入biao_zhi_wei函数
from gongneng import xun_heikuang                    # 从gongneng模块导入xun_heikuang函数
from reset import hui_zhongdian,jiaozhun             # 从reset模块导入hui_zhongdian函数,jiaozhun函数

angle=[]

while(True):
    b = biao_zhi_wei()                               # 由b存放标识位列表
    if b==[65,66,0,0,0,0,0,1,0]:
        angle=jiaozhun()                             # 舵机校准
    if b==[65,66,1,0,0,0,0,0,0]:
        hui_zhongdian()                              # 舵机复位
    if b==[65,66,0,1,0,0,0,0,0]:
        sao_bianxian()                               # 扫边框
    if b==[65,66,0,0,1,0,0,0,0]:
        xun_heikuang()                               # 循黑线
