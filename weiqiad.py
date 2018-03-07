# coding: utf-8
import os
import sys
import subprocess
import shutil
import time
import math
from PIL import Image, ImageDraw
import random
import json
import re
import msvcrt

cx=[]#棋盘线像素位置
cy=[]#棋盘线像素位置
cc=[[]]#棋盘坐标像素位置
cb=[[]]#棋盘坐标
cs=[[]]#棋谱坐标
#腾讯围棋对局棋盘坐标，其中y轴会可能会下降25像素
#cx=[47,120,197,271,345,419,496,569,644,721,795,869,944,1020,1094,1168,1243,1319,1392]
cy0=[425,497,574,648,722,796,872,946,1020,1098,1172,1246,1320,1396,1471,1545,1620,1696,1769]
#cy= [x+25 for x in cy0]#调整人机对战棋盘
#cy=cy0
cxa=['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T']
#cya1=[19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
cya=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
#boardcolor=(93, 69, 47, 255)#腾讯
boardcolor=(0, 0, 0, 255)#弈城
moveconfirm=True #确认走子
#proc = subprocess.Popen('D:\\Leela0110GTP\\1_Leela0110GTP_OpenCL.exe -g -p 5000 --noponder -q', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#proc = subprocess.Popen()
def chessboard(im):
    x,y=im.size
    imp=im.load()
    getlt=False
    getrd=False
    for i in range(10,int(x*0.05),1):
        for j in range(100,int(y*0.3),1):
            if imp[i,j]==imp[i+20,j]==imp[i,j+20]==boardcolor:
                x0=i
                y0=j
                getlt=True
                break
        if getlt==True:
            break
        
    for i in range(x-10,int(x*19/20),-1):
        for j in range(int(y*0.8),int(y*0.64),-1):
            if imp[i,j]==imp[i-20,j]==imp[i,j-20]==boardcolor:
                x1=i
                y1=j
                getrd=True
                break
        if getrd==True:
            break
    return x0,y0,x1,y1
  


#返回电脑走棋的棋盘坐标   
def genmove(color):
    cmd = ("genmove "+color+"\n").encode('utf-8')
    print(cmd)
    proc.stdin.write(cmd)
    proc.stdin.flush()
    a=proc.stdout.readline()
    proc.stdout.readline()#read the blank line
    #proc.stdout.flush()
    a=a.decode('utf-8')
    a=a.strip()
    a=a.lstrip('= ')
    print(a)
    return a

#读取进程p的控制台输出信息，以空白行为终止条件
def stdreadlines(p):
    while True:
        try:
            line = p.stdout.readline() #如果p.stdout中内容被读完之后，程序会卡在这里 
            if line == b'\r\n': 
                break #
        #l=line.decode('gb18030')
            l=line.decode()
            l = l.strip() 
            print(l)
        except IOError:
            break
#读取进程p的控制台输出信息，以空白行为终止条件
def runCommand(p,cmd):
    print(cmd)
    proc.stdin.write((cmd+'\n').encode('utf-8'))
    proc.stdin.flush()
    while True:
        try:
            line = p.stdout.readline() #如果p.stdout中内容被读完之后，程序会卡在这里 
            if line == b'\r\n': 
                break #
        #l=line.decode('gb18030')
            l=line.decode()
            l = l.strip() 
            print(l)
        except IOError:
            break        
#将对方走子输入AI，play B O14
def play(c,p):
    cmd=("play "+str(c)+" "+str(p)+"\n").encode('utf-8')
    print(cmd)
    proc.stdin.write(cmd)
    proc.stdin.flush()
    proc.stdout.readline()
    proc.stdout.readline()#read the blank line
    return
    
#根据棋盘坐标返回腾讯围棋棋盘的像素坐标    
def convertxy(p):
    xs=p.rstrip('0123456789')
    x,y=1,1
    for i in range(19):
        if xs==cxa[i]:
            x=cx[i]
            break
    ys=p.lstrip('ABCDEFGHIJKLMNOPQRST')
    for i in range(19):
        if int(ys)==cya[i]:
            y=cy[i]
            break
    return(x,y)
    
#根据棋盘坐标在手机上走棋
def move(o):
    #press_time = 200
    x,y=convertxy(o)
    cmd = 'adb shell input tap {x1} {y1}'.format(
        x1=x,
        y1=y
    )
    print('move into {}'.format(o))
    os.system(cmd)
    if moveconfirm:
        cmd = 'adb shell input tap {x1} {y1}'.format(
        x1=750,
        y1=2180
        )
        os.system(cmd)
        
          
    
#将棋盘坐标转换为棋谱坐标   
def convert(p):
    x=p.rstrip('0123456789')
    x=x.lower()
    if x>='j':
        x=chr(ord(x)-1)        
    y=p.lstrip('ABCDEFGHIJKLMNOPQRST')
    return x+chr(int(y)+96)
    
def playSelf():
    print("(;CA[gb2312]SZ[19]AP[leela]")
    while True:
        b=genmove('black')
        print(';B['+b+']',end='')
        w=genmove('white')
        print(';w['+w+']',end='')
        time.sleep(1)

def _get_screen_size():
    size_str = os.popen('adb shell wm size').read()
    m = re.search('(\d+)x(\d+)', size_str)
    if m:
        width = m.group(1)
        height = m.group(2)
        return "{height}x{width}".format(height=height, width=width)

def pull_screenshot():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open('meweiqi.png', 'wb')
    f.write(screenshot)
    f.close()


def set_button_position(im):
    # 将swipe设置为 `再来一局` 按钮的位置
    global swipe_x1, swipe_y1, swipe_x2, swipe_y2
    w, h = im.size
    left = w / 2
    top = 1003 * (h / 1280.0) + 10
    swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, left, top


def dump_device_info():
    size_str = os.popen('adb shell wm size').read()
    device_str = os.popen('adb shell getprop ro.product.model').read()
    density_str = os.popen('adb shell wm density').read()
    print("如果你的脚本无法工作，上报issue时请copy如下信息:\n**********\
        \nScreen: {size}\nDensity: {dpi}\nDeviceType: {type}\nOS: {os}\nPython: {python}\n**********".format(
            size=size_str.strip(),
            type=device_str.strip(),
            dpi=density_str.strip(),
            os=sys.platform,
            python=sys.version
    ))

def check_adb():
    flag = os.system('adb devices')
    if flag == 1:
        print('请安装ADB并配置环境变量')
        sys.exit()
#扫描并返回当前截图的最近走子颜色与位置
def scanqizi(im):
    impix=im.load()
    #imd=ImageDraw.Draw(im)
    global cx,cy,cxa,cya
    for i in range(19):
        for j in range(19): 
            ip1=impix[cx[i]-6,cy[j]-6] 
            ip2=impix[cx[i]+8,cy[j]+8]
            yy1=ip1[0]+ip1[1]+ip1[2]#棋子左上点像素值
            yy2=ip2[0]+ip2[1]+ip2[2]#棋子右下点像素值，判断新子               
            if yy1<120:#有黑棋
                if yy2>600:#黑棋为最近一手
                    color='B'
                    p=str(cxa[i])+str(cya[j])
                    #print(p,color,yy1,yy2) 
                    return color,p,yy1,yy2
            if yy1>600:#有白棋
                if yy2<120:#白棋为最近一手
                    color='W'
                    p=str(cxa[i])+str(cya[j])
                    #print(p,color,yy1,yy2) 
                    return color,p,yy1,yy2
    return 'e','e',0,0
def save_debugscreen():
    global cx,cy,cc,cxa,cya
    pull_screenshot()
    im = Image.open('./meweiqi.png')
    x0,y0,x1,y1=chessboard(im)
    cx=[x0+int((x1-x0)*i/18) for i in range(19)]
    cy=[y0+int((y1-y0)*i/18) for i in range(19)]
    cc=[[[x,y] for y in cy] for x in cx]
    print(cx)
    print(cy)
    imd=ImageDraw.Draw(im)    
    for i in range(19):
        for j in range(19): 
            #绘制参考线
            imd.ellipse((cx[i]-10, cy[j]-10, cx[i]+10, cy[j]+10),fill=(255, 0, 0)) 
    #cboard=[{x0+int((x1-x0)*i/19),y0+int((y1-y0)*i/19)} for i in range(1,20,1)]
    
    ts = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    im.save('debugscreen{}.png'.format(ts))
#写入棋谱文件
def writeSGF(f,c,p):
    pp=convert(p)
    f.write(';{0}[{1}]\n'.format(c,pp))
    f.flush()
    
def main():
    global proc    
    proc = subprocess.Popen('D:\\Leela0110GTP\\1_Leela0110GTP_OpenCL.exe -g -p 5000 --noponder -q', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    loop=True
    lastp='A1'#最近一手位置
    AIcolor='B'#AI的颜色
    ecolor='W'#对手的颜色       
    ts = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    f=open('{0}.sgf'.format(ts),'a')
    f.write("(;CA[gb2312]SZ[19]AP[leela]")
    f.write("\n") 
    
    #选择AI的颜色
    while True:
        print("\n\nPress w or b for choose white or black.\n")
        x=msvcrt.getch()
        if x==b'w'  or x==b'W':
            AIcolor='W'
            ecolor='B'
            save_debugscreen()
            break
        if x==b'B' or x==b'b':
            AIcolor='B'
            ecolor='W'
            save_debugscreen()
            o=genmove(AIcolor)
            writeSGF(f,AIcolor,o)
            #print(o)
            move(o)
            lastp=o#更新最新位置
            break
        print("Input error, please input again!")
    try:
        while loop:
            #loop=False        
            pull_screenshot()        
            im = Image.open('./meweiqi.png')
            color,p,y1,y2 = scanqizi(im)        
            if p!=lastp and p!='e' and color==ecolor:
                print(color,p,y1,y2)
                lastp=p
                writeSGF(f,ecolor,p)
                play(ecolor,p)            
                #time.sleep(1)
                o=genmove(AIcolor)            
                move(o)
                writeSGF(f,AIcolor,o)
                lastp=o#更新最新位置
                runCommand(proc,'winrate')
                time.sleep(5)
                print(("Scan {0}.").format(ecolor),end='',flush=True)
            else:
                time.sleep(3)
                print(".",end='',flush=True)
                #print(p)
    except KeyboardInterrupt as e:
            print('收到结束信号，正在处理重置')
            loop=False
            #proc = subprocess.Popen('Leela0110GTP.exe -g -p 5000 --noponder -q', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            main()
if __name__ == '__main__':
    dump_device_info()
    check_adb()
    main()
