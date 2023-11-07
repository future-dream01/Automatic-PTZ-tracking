# 全部功能函数

import sensor, image, time, math,time,lcd ,pyb       # 导入函数所依赖的模块：传感器、图像、定时器模块、数学函数模块(python标准库)、时间模块(追踪运行时间)
from pid import Pid                                  # 从pid模块导入Pid类
from pyb import Servo                                # 从pyb模块引入Servo类
from shuju import biao_zhi_wei                       # 从shuju模块中导入biao_zhi_wei函数
from reset import hui_zhongdian
s1=Servo(1)                                          # 初始化舵机s1
s2=Servo(2)                                          # 初始化舵机s2
global angle

#######################################################################################################################################

def find_max1(rects):
    # 定义一个find_max1()函数，用来返回画面中最大的一个矩形的信息，参数是画面中所有矩形组成的列表
    max_size=0                                      # 初始化max_size
    for rect in rects:                              # 对于rects列表里面的所有色块做遍历
        if (rect[2]*rect[3] > max_size):
            max_rect=rect
            max_size = rect[2]*rect[3]              # 如矩形的横长和竖高的乘积（即面积）大于max_size，就把这个矩形赋给max_size，相当于是一个取大函数
    return max_rect                                 # 返回最大的矩形的信息列表

#######################################################################################################################################

def find_max2(blobs):
    # 定义一个find_max2()函数，用来返回画面中最大的一个色块的信息，参数是画面中所有色快组成的列表
    max_size=0                                      # 初始化max_size
    for blob in blobs:                              # 对于blobs列表里面的所有色块做遍历
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]              # 如果色块的横长和竖高的乘积（即面积）大于max_size，就把这个色块赋给max_size，相当于是一个取大函数
    return max_blob                                 # 返回最大的色块的信息列表

#######################################################################################################################################

def insert_a_uniformly_into_b(a, b):
    # 数组插入函数
    n = len(b) // len(a)
    new_array = []
    for i in range(len(a)):
        new_array.append(a[i])
        new_array.extend(b[i * n : (i + 1) * n])
    return new_array

#######################################################################################################################################

def xun_heikuang():
    # 巡黑框函数
    sensor.reset()                                  # 初始化相机传感器
    sensor.set_pixformat(sensor.RGB565)             # 设置相机模块的像素模式（此处为RGB6565模式）.
    sensor.set_framesize(sensor.QVGA)               # 设置相机模块的帧大小（此处为QQVGA）.
    sensor.skip_frames(time=2000)                   # 改变相机设置后通过跳过指定帧数或延时指定时间来等待相机图像稳定（此处延时2000毫秒）.
    sensor.set_auto_gain(False)                     # 自动增益（可能改变颜色阈值涉及颜色识别功能则选择关闭）.
    sensor.set_auto_whitebal(False)                 # 白平衡设置（可能改变颜色阈值涉及颜色识别功能则选择关闭）.
    sensor.set_auto_exposure(False,40000)           # 曝光设置
    sensor.set_contrast(3)                          # 对比度设置
    sensor.set_brightness(-3)                       # 亮度
    clock = time.clock()                            # 调用time模块中的clock()函数,定义clock变量为一个时钟对象，存放从某一时间点开始的经过时间.
    thresholds = [(63, 100, 127, 7, -109, 105),     # 红色的颜色阈值列表
                  (30, 100, -64, -8, -32, 32),      # 绿色的颜色阈值列表
                  (0, 4, 61, -36, 2, -74)]          # 黑框的颜色阈值
    w_pid=Pid(p=0.041,i=0.98,d=0)                   # 设置水平方向上的p、i、d参数
    h_pid=Pid(p=0.041 ,i=0.98,d=0)                  # 设置竖直方向上的p、i、d参数
    dingdian1=[0]                                   # 初始化dingdian1顶角列表
    dingdian2=[]                                    # 初始化dingdian2插入点列表
    dingdian=[]                                     # 初始化总点列表
    N=0                                             # 每条边插入点的数目
    c=2                                             # 离开顶点阈值
    f=0                                             # 初始化总点列表索引
    while(True):
        b=biao_zhi_wei()                            # 接受uart数据，随时暂停或暂停后继续
        while(b==[65,66,0,0,0,1,0,0,0]):
            b=biao_zhi_wei()
            if b==[65,66,0,0,0,0,1,0,0]:
                break
        clock.tick()                                # 开始跟踪运行时间
        # img = sensor.snapshot().binary([(0, 4, 61, -36, 2, -74)]).lens_corr(1.8) #使用相机拍摄一张照片，并返回 image 对象，赋给img变量 .
        img = sensor.snapshot().lens_corr(1.8) # 相机拍照，畸变矫正
        # img.draw_cross(80,60,(0,255,0),scale=4)    # 画面中心位置画十字
        # blobs = img.find_blobs([thresholds[threshold_index]], pixels_threshold=2, area_threshold=2, merge=True)
        # find_blobs()方法查找图像中所有色块，并返回以所有色块信息为元素的列表，赋给blobs
        # 第一个参数：根据前面 threshold_index 的值访问 thresholds 列表中的对应元素
        # 第二个参数：pixels_threshold：像素个数阈值，如果色块像素数量小于这个值，会被过滤掉
        # 第三个参数：area_threshold：面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
        # 第四个参数：merge：合并，如果设置为True，那么合并所有重叠的blob为一个，即吧所有色块当成一个大色块处理
        # rects = img.find_rects(threshold=25000,roi=(47,43,76,72))
        # find_rects():对图像对象使用find_rects()方法，返回一个真正的矩形对象，赋给r；使用用于查找AprilTAg的相同的quad detection算法来查找图像中的矩形，返回一个矩形对象给r
        # threshold应设置为足够高的值，以滤除在图像中检测到的具有低边缘幅度的噪声矩形，最适用与背景形成鲜明对比的矩形。
        # roi设置感兴趣的区域
        while(dingdian1==[0]):
            img = sensor.snapshot().binary([thresholds[2]])
            # 将黑框二值化，增加与背景的区分度，有利于识别矩形
            # img.midpoint(1, bias=0.9, threshold=True, offset=5, invert=True)
            rects = img.find_rects(threshold=100000,roi=(40,17,238,202))
            # 对img对象使用find_rects()方法，依次找到画面中的所有矩形，返回一个包含这个矩形的x、y、w、h、矩形的模的列表
            # threshold 参数过滤矩形，只有像素大小大于这个值的矩形才会被识别
            # roi：感兴趣区域
            if rects:                                                       # 如果识别到矩形
                r = find_max1(rects)                                        # 找出画面中最大的矩形
                dingdian1=r.corners()                                       # 将四个顶点的坐标一次写入dingdian1列表
                for q in range(0,4):                                        # 获取所有插入的点的x，y坐标元组组成的列表
                    if q==3:
                        q=-1
                    j=int((dingdian1[q+1][0]-dingdian1[q][0])/(N+1))
                    k=int((dingdian1[q+1][1]-dingdian1[q][1])/(N+1))
                    for p in range(1,N+1):
                        if q==-1:
                            q=3
                        dingdian2.append((dingdian1[q][0]+p*j,dingdian1[q][1]+p*k))
                dingdian=insert_a_uniformly_into_b(dingdian1,dingdian2)     # 将顶点列表插入插入点列表
                print (dingdian)
        img.draw_edges(r.corners(),(255,0,0),thickness=1)                   # 画出检测到的矩形的边框
        img = sensor.snapshot().lens_corr(1.8)                              # 重设img变量
        blobs = img.find_blobs([thresholds[0]], pixels_threshold=2, area_threshold=2, merge=True)
        if blobs:
            s=find_max2(blobs)                                              # 找出画面中最大的色块
            img.draw_rectangle(s.rect(),thickness=3)                        # 作矩形框，rect()方法返回一个物体的外接水平矩形的的元组(x,y,w,h)
            img.draw_cross(s.cx(), s.cy(),thickness=3)                      # 在图像上绘制十字，接受的参数分别是色块中心位置的x坐标和y坐标
            w_error=s.cx()-dingdian[f][0]                                   # 获取水平方向上和目标矩形其中之一顶点坐标之间的水平偏差
            h_error=s.cy()-dingdian[f][1]                                   # 获取竖直方向上和目标矩形其中之一顶点坐标之间的竖直偏差
            a=s.cx()                                                        # 将每一次的坐标值存入变量中，防止出现识别不到色块而导致的没有数据传给pid的情况
            t=s.cy()
            img.draw_string(100,90,str(w_error),color=(0,255,0))            # 规定位置写出水平误差值
            img.draw_string(100,100,str(h_error),color=(0,255,0))           # 规定位置写出竖直误差值
            w_output = w_pid.get_pid(w_error*0.8)                           # 将水平偏差输入get_pid()函数，获取修正值
            h_output = -h_pid.get_pid(h_error*0.8)                          # 将竖直偏差输入get_pid()函数，获取修正值
            s1.angle(w_output)                                              # s1舵机转动指定角度
            s2.angle(h_output)                                              # s2舵机转动指定角度
        else :                                                              # 对于没有识别到色块的情况，沿用上一次识别到的数据代替此次数据
            w_error=a-dingdian[f][0]                                        # 获取水平方向上和目标矩形其中之一顶点坐标之间的水平偏差
            h_error=t-dingdian[f][1]                                        # 获取竖直方向上和目标矩形其中之一顶点坐标之间的竖直偏差
            img.draw_string(100,90,str(w_error),color=(0,255,0))            # 规定位置写出水平误差值
            img.draw_string(100,100,str(h_error),color=(0,255,0))           # 规定位置写出竖直误差值
            w_output = w_pid.get_pid(w_error)                               # 将水平偏差输入get_pid()函数，获取修正值
            h_output = -h_pid.get_pid(h_error)                              # 将竖直偏差输入get_pid()函数，获取修正值
            s1.angle(w_output)                                              # s1舵机转动指定角度
            s2.angle(h_output)                                              # s2舵机转动指定角度
        if((w_error>=-c and w_error<=c)and(h_error>=-c and h_error<=c)):    # 如果色块到达顶点位置
            f+=1
            if f==4+N*4:
                f=0
        print(clock.fps()) # 停止追踪运行时间，并返回当前FPS（每秒帧数）

#######################################################################################################################################

def genzong_sekuai():
    #色块跟踪函数
    sensor.reset()                                 # 初始化相机传感器
    sensor.set_pixformat(sensor.RGB565)            # 设置相机模块的像素模式（此处为RGB6565模式）.
    sensor.set_framesize(sensor.CIF)               # 设置相机模块的帧大小（此处为QQVGA）.
    sensor.skip_frames(time=500)                   # 改变相机设置后通过跳过指定帧数或延时指定时间来等待相机图像稳定（此处延时2000毫秒）.
    sensor.set_auto_gain(False)                    # 自动增益（可能改变颜色阈值涉及颜色识别功能则选择关闭）.
    sensor.set_auto_whitebal(False)                # 白平衡设置（可能改变颜色阈值涉及颜色识别功能则选择关闭）.
    sensor.set_vflip(True)                         # 水平翻转
    sensor.set_hmirror(True)                       # 竖直翻转
    sensor.set_auto_exposure(False,17000)          # 曝光设置
    sensor.set_contrast(3)                         # 对比度设置
    sensor.set_brightness(-3 )                     # 亮度设置
    clock = time.clock()                           # 调用time模块中的clock()函数,定义clock变量为一个时钟对象，存放从某一时间点开始的经过时间.
    s1=Servo(1)                                    # s1舵机初始化
    s2=Servo(2)                                    # s2舵机初始化
    thresholds = [(6, 92, 17, 93, -47, 68),        # 红色的颜色阈值列表
                  (30, 100, -64, -8, -32, 32),     # 绿色的颜色阈值列表
                  (0, 30, 0, 64, -128, 0)]         # 蓝色的阈值列表
    w_pid=Pid(p=0.07,i=1.8,d=0)                    # 设置水平方向上的p、i、d参数
    h_pid=Pid(p=0.07,i=1.8,d=0)                    # 设置竖直方向上的p、i、d参数
    s1.angle(0)                                    # 复位
    s2.angle(0)                                    # 复位
    pyb.delay(500)                                 # 延时，防止受干扰

    while(True):
        while(True):                               # 接受uart数据，随时暂停或暂停后继续
            b=biao_zhi_wei()
            while(b==[65,66,0,0,1,0,0,0,0]):
                b=biao_zhi_wei()
                if b==[65,66,0,0,0,1,0,0,0]:
                    break
        clock.tick()                               # 开始跟踪运行时间
        img = sensor.snapshot()                    # 使用相机拍摄一张照片，并返回 image 对象，赋给img变量
        blobs = img.find_blobs([thresholds[0]], pixels_threshold=7, area_threshold=7, merge=True)
        # find_blobs()方法查找图像中所有色块，并返回以所有色块信息为元素的列表，赋给blobs
        # 第一个参数：根据前面 threshold_index 的值访问 thresholds 列表中的对应元素
        # 第二个参数：pixels_threshold：像素个数阈值，如果色块像素数量小于这个值，会被过滤掉
        # 第三个参数：area_threshold：面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉
        # 第四个参数：merge：合并，如果设置为True，那么合并所有重叠的blob为一个，即吧所有色块当成一个大色块处理
        if blobs:
            max_blob=find_max2(blobs) #找出画面中最大的色块
            # img.draw_edges(max_blob.min_corners(), color=(255,0,0))
            # draw_edges()绘制最小面积矩形，此矩形可随色块在图像中的角度任意倾斜，不同于矩形白框只能横平竖直
            # 参数一：min_corners()方法返回最小面积矩形四个角的坐标元组列表[(x1, y1), (x2, y2), (x3, y3), (x4、y4)]
            # 参数二：要绘制的矩形线边的颜色，通过颜色阈值三元组颜色阈值(x,y,z)表示,六元组颜色阈值可以更精确的表示阴影、饱和度、亮度，三元组则更简洁
            # img.draw_line(max_blob.major_axis_line(), color=(0,255,0))
            # draw_line()方法做出一条线段
            # 参数一：major_axis_line()方法返回通过色块最小面积矩形中心且与最小面积矩形最长边平行且相等线段的起点终点坐标元组
            # 参数二：要绘制的线段的颜色
            # img.draw_line(max_blob.minor_axis_line(), color=(0,0,255))
            # draw_line()方法做出一条线段
            # 参数一：minor_axis_line()方法返回通过色块最小面积矩形中心且与最小面积矩形最短边平行且相等线段的起点终点坐标元组
            # 参数二：要绘制的线段的颜色
            img.draw_rectangle(max_blob.rect(),thickness=3)         # 作矩形框，rect()方法返回一个物体的外接水平矩形的的元组(x,y,w,h)
            img.draw_cross(max_blob.cx(), max_blob.cy())            # 在图像上绘制十字，接受的参数分别是色块中心位置的x坐标和y坐标
            # img.draw_keypoints([(max_blob.cx(), max_blob.cy(), int(math.degrees(max_blob.rotation())))], size=20)
            # draw_keypoints()方法：绘制一个具有特定方向线(较细长物体效果更显著)的圆
            # 第一、第二个参数：分别传入色块中心点的x、y坐标
            # 参数三：degrees()方法返回特定弧度对应的度数，rotation()方法返回返回色块的旋转弧度，两者共同绘制细长物体方向的方向线
            # 参数四：size控制圆和方向线的大小
            w_error=max_blob.cx()-183                               # 获取水平方向上和画面中心点之间的偏差
            h_error=max_blob.cy()-163                               # 获取竖直方向上和画面中心点之间的偏差
            if( w_error<=3 and w_error>=-3) and ( h_error<=3 and h_error>=-3):
                w_error=0
                h_error=0
            img.draw_string(100,90,str(w_error),color=(0,255,0))
            # draw_string()方法：在图像上显示指定字符串
            # 参数一、参数二：字符串左端点的x、y坐标(图像区域左下角为坐标原点)
            # 参数三：设置字符串颜色
            img.draw_string(100,100,str(h_error),color=(0,255,0))
            w_output = -w_pid.get_pid(w_error)                      # 将水平偏差输入get_pid()函数，获取修正值
            h_output = -h_pid.get_pid(h_error)                      # 将竖直偏差输入get_pid()函数，获取修正值
            s1.angle(w_output)
            s2.angle(h_output)
            # 将水平修正值和竖直修正值由uart.write()方法发送给单片机
            # bytearray()函数将其内的参数转化为16进制列表的形式
            # w_output和h_output默认为float型，但是bytearray()函数参数需要为整型，所以需要强制类型转换
        print(clock.fps())                                          # 停止追踪运行时间，并返回当前FPS（每秒帧数）

#######################################################################################################################################

def sao_bianxian(a):
    # 扫幕布外围的铅笔线,参数a是舵机的角度
    s1.angle(angle[2],500)
    s2.angle(angle[3],500)
    pyb.delay(1000)
    s1.angle(angle[4],500)
    s2.angle(angle[5],500)
    pyb.delay(1000)
    s1.angle(angle[6],500)
    s2.angle(angle[7],500)
    pyb.delay(1000)
    s1.angle(angle[8],500)
    s2.angle(angle[9],500)
    pyb.delay(1000)
#hui_zhongdian()
#while(True):
    #sao_bianxian(a=15)
#xun_heikuang()
