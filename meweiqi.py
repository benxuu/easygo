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


#腾讯围棋人工对局坐标，人机对战y轴会下降25像素
cx=[47,120,197,271,345,419,496,569,644,721,795,869,944,1020,1094,1168,1243,1319,1392]
cy0=[425,497,574,648,722,796,872,946,1020,1098,1172,1246,1320,1396,1471,1545,1620,1696,1769]
#cy= [x+25 for x in cy0]#调整人机对战棋盘
cy=cy0
cxa=['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T']
#cya1=[19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
cya=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]


proc = subprocess.Popen('D:\\Leela0110GTP\\1_Leela0110GTP_OpenCL.exe -g -p 1000 --noponder -q', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)


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
#将对方走子输入AI，play B O14
def play(c,p):
    cmd=("play "+str(c)+" "+str(p)+"\n").encode('utf-8')
    print(cmd)
    proc.stdin.write(cmd)
    proc.stdin.flush()
    proc.stdout.readline()
    proc.stdout.readline()#read the blank line
    #proc.stdout.flush()
    #a=a.decode('utf-8')
    #a=a.strip()
    #a=a.lstrip('= ')    
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
    
#根据棋盘坐标走棋
def move(o):
    #press_time = 200
    x,y=convertxy(o)
    cmd = 'adb shell input tap {x1} {y1}'.format(
        x1=x,
        y1=y
    )
    print(cmd)
    os.system(cmd)           
    
    
def convert(p):
    #p=position.strip()
    #p=p.lstrip('= ')
    x=p.rstrip('0123456789')
    x=x.lower()
    if x=='j':
        x='i'
    elif x=='k':
        x='j'
    elif x=='l':
        x='k'
    elif x=='m':
        x='l'
    elif x=='n':
        x='m'
    elif x=='o':
        x='n'
    elif x=='p':
        x='o'
    elif x=='q':
        x='p'
    elif x=='r':
        x='q'
    elif x=='s':
        x='r'
    elif x=='t':
        x='s'
        
    y=p.lstrip('ABCDEFGHIJKLMNOPQRST')
    
    if y=='1':
        return x+'s'
    elif y=='2':
        return x+'r'
    elif y=='3':
        return x+'q'
    elif y=='4':
        return x+'p'
    elif y=='5':
        return x+'o'
    elif y=='6':
        return x+'n'
    elif y=='7':
        return x+'m'
    elif y=='8':
        return x+'l'
    elif y=='9':
        return x+'k'
    elif y=='10':
        return x+'j'
    elif y=='11':
        return x+'i'
    elif y=='12':
        return x+'h'
    elif y=='13':
        return x+'g'
    elif y=='14':
        return x+'f'
    elif y=='15':
        return x+'e'
    elif y=='16':
        return x+'d'
    elif y=='17':
        return x+'c'
    elif y=='18':
        return x+'b'
    elif y=='19':
        return x+'a'

def playSelf():
    print("(;CA[gb2312]SZ[19]AP[leela]")
    while True:
        b=genmove('black')
        print(';B['+b+']',end='')
        w=genmove('white')
        print(';w['+w+']',end='')
        time.sleep(1)

def open_accordant_config():
    screen_size = _get_screen_size()
    config_file = "{path}/config/{screen_size}/config.json".format(
        path=sys.path[0],
        screen_size=screen_size
    )
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("Load config file from {}".format(config_file))
            return json.load(f)
    else:
        with open('{}/config/default.json'.format(sys.path[0]), 'r') as f:
            print("Load default config")
            return json.load(f)


def _get_screen_size():
    size_str = os.popen('adb shell wm size').read()
    m = re.search('(\d+)x(\d+)', size_str)
    if m:
        width = m.group(1)
        height = m.group(2)
        return "{height}x{width}".format(height=height, width=width)


config = open_accordant_config()

# Magic Number，不设置可能无法正常执行，请根据具体截图从上到下按需设置
under_game_score_y = config['under_game_score_y']
press_coefficient = config['press_coefficient']       # 长按的时间系数，请自己根据实际情况调节
piece_base_height_1_2 = config['piece_base_height_1_2']   # 二分之一的棋子底座高度，可能要调节
piece_body_width = config['piece_body_width']             # 棋子的宽度，比截图中量到的稍微大一点比较安全，可能要调节

# 模拟按压的起始点坐标，需要自动重复游戏请设置成“再来一局”的坐标
if config.get('swipe'):
    swipe = config['swipe']
else:
    swipe = {}
    swipe['x1'], swipe['y1'], swipe['x2'], swipe['y2'] = 320, 410, 320, 410


screenshot_backup_dir = 'screenshot_backups/'
if not os.path.isdir(screenshot_backup_dir):
        os.mkdir(screenshot_backup_dir)


def pull_screenshot():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open('meweiqi.png', 'wb')
    f.write(screenshot)
    f.close()

def backup_screenshot(ts):
    # 为了方便失败的时候 debug
    if not os.path.isdir(screenshot_backup_dir):
        os.mkdir(screenshot_backup_dir)
    shutil.copy('meweiqi.png', '{}{}.png'.format(screenshot_backup_dir, ts))


def save_debug_screenshot(ts, im, piece_x, piece_y, board_x, board_y):
    draw = ImageDraw.Draw(im)
    # 对debug图片加上详细的注释
    draw.line((piece_x, piece_y) + (board_x, board_y), fill=2, width=3)
    draw.line((piece_x, 0, piece_x, im.size[1]), fill=(255, 0, 0))
    draw.line((0, piece_y, im.size[0], piece_y), fill=(255, 0, 0))
    draw.line((board_x, 0, board_x, im.size[1]), fill=(0, 0, 255))
    draw.line((0, board_y, im.size[0], board_y), fill=(0, 0, 255))
    draw.ellipse((piece_x - 10, piece_y - 10, piece_x + 10, piece_y + 10), fill=(255, 0, 0))
    draw.ellipse((board_x - 10, board_y - 10, board_x + 10, board_y + 10), fill=(0, 0, 255))
    del draw
    im.save('{}{}_d.png'.format(screenshot_backup_dir, ts))


def set_button_position(im):
    # 将swipe设置为 `再来一局` 按钮的位置
    global swipe_x1, swipe_y1, swipe_x2, swipe_y2
    w, h = im.size
    left = w / 2
    top = 1003 * (h / 1280.0) + 10
    swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, left, top


def jump(distance):
    press_time = distance * press_coefficient
    press_time = max(press_time, 200)   # 设置 200 ms 是最小的按压时间
    press_time = int(press_time)
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=swipe['x1'],
        y1=swipe['y1'],
        x2=swipe['x2'],
        y2=swipe['y2'],
        duration=press_time
    )
    print(cmd)
    os.system(cmd)




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
def save_debugscreen(im):
    global cx,cy,cxa,cya
    imp=im.load()
    #计算并消除y向偏差
    for i in range(400,460,1):
        ip=imp[60,i]
        if ip[0]==93 and ip[1]==69:
            cy=[x+i-425 for x in cy0]#调整人机对战棋盘
            print('已调整坐标偏差',i-425)
            print(cx)
            print(cy)
            break            
    imd=ImageDraw.Draw(im)    
    for i in range(19):
        for j in range(19): 
            #绘制参考线
            imd.ellipse((cx[i]-10, cy[j]-10, cx[i]+10, cy[j]+10),fill=(255, 0, 0)) 
    ts = int(time.time())
    im.save('debugscreen{}.png'.format(ts))
    
def main():
    dump_device_info()
    check_adb()
    loop=True
    lastp='A1'#最近一手位置
    AIcolor='B'#AI的颜色
    ecolor='W'#对手的颜色
    pull_screenshot()        
    im = Image.open('./meweiqi.png')
    save_debugscreen(im)
    #选择AI的颜色
    while True:
        x=input("\n\nInput w or b for choose white or black.\n")
        if x=="w"  or x=="W":
            AIcolor='W'
            ecolor='B'
            break
        if x=="B"or x=="b":
            AIcolor='B'
            ecolor='W'
            o=genmove(AIcolor)
            #print(o)
            move(o)
            lastp=o#更新最新位置
            break
        print("Input error, please input again!")
        
           
    while loop:
        #loop=False        
        pull_screenshot()        
        im = Image.open('./meweiqi.png')
        color,p,y1,y2 = scanqizi(im)
        if p!=lastp and p!='e':
            print(color,p,y1,y2)
            lastp=p
            play(ecolor,p)
            #time.sleep(1)
            o=genmove(AIcolor)
            move(o)
            lastp=o#更新最新位置
            time.sleep(6)
        else:
            time.sleep(4)
            #print(p)
if __name__ == '__main__':
    main()
