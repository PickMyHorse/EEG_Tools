import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
import os
import keyboard
from scipy.signal import butter, filtfilt
from tqdm import tqdm
import time
fs = 256

import shutil

fig1 = plt.figure(figsize=(15, 3))
plt.ylim(-120, 120)
# 自定义Y轴刻度
yticks_values = [-120, -100, -80, -60, -50, -40, -20, 0, 20, 40, 50, 60, 80, 100, 120]
plt.yticks(yticks_values)

# 在+-50处加红色横线
plt.axhline(y=50, color='red', linestyle='--')
plt.axhline(y=-50, color='red', linestyle='--')

# 在+-100处加***横线
plt.axhline(y=100, color='crimson', linestyle='-.')
plt.axhline(y=-100, color='crimson', linestyle='-.')
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
for j in range(1, 5):
    plt.axvline(x=j * 512, color='k', linestyle='--')
line, = plt.plot(0, 0)
plt.tight_layout()
# 获取当前图形窗口管理器并设置窗口位置
fig_manager = plt.get_current_fig_manager()
fig_manager.window.wm_geometry("+0+0")  # 将窗口显示在屏幕左上角
ax = plt.gca()
plt.ion()
plt.show()

times = 0

def label_make(seq_num, signal, epoch_length, epoch_num):
    global times  # 声明'time'为全局变量
    segment_length = len(signal)
    plt.xlim(0, segment_length)

    line.set_data(np.arange(segment_length), signal)  # 更新plot对象的数据
    plt.title("Seq {} Waveform".format(seq_num + 1))
    ax.set_facecolor(None)
    times += 1
    if times % 2 == 1:
        ax.set_facecolor('lightgray')
    else:
        ax.set_facecolor('white')
    
    plt.draw()  # 重绘图形
    plt.pause(0.3)  # 等待键盘输入
    epoch_label = [0, 0, 0, 0, 0]
    label = None

    # 等待用户按下左右方向键
    while not label:
        if keyboard.is_pressed('right'):
            print(epoch_label)
            return epoch_label  
        elif keyboard.is_pressed('left'):
            epoch_label = [1, 1, 1, 1, 1]
            print(epoch_label)
            return epoch_label 
        elif keyboard.is_pressed('0'):
            for m in range(epoch_num):
                label1 = None
                print("input label of epoch {}(黄色部分):".format(m + 1))
                print("INPUT label :")
                rect1 = ax.axvspan(m*512, (m+1)*512, facecolor='yellow', alpha=0.5)
                rect2 = ax.axvspan((m+1)*512, 5*512, facecolor='white', alpha=0.5)
                rect3 = ax.axvspan(0, m*512, facecolor='white', alpha=0.5)
                plt.draw()
                plt.pause(0.3)  # 等待键盘输入
                while label1 is None:
                    if keyboard.is_pressed('up'):
                        label1 = 1
                    elif keyboard.is_pressed('down'):
                        label1 = 0
                print("label is :", label1)
                epoch_label[m] = label1
                rect1.remove()
                rect2.remove()
                rect3.remove()
    print(epoch_label)
    return epoch_label

# 以下是文件处理部分
folder_path = "C:/Users/12944/Desktop/1/asd_single/epoch/"
file_list = os.listdir(folder_path)
s_path = folder_path + "labeled/"
for file_name in file_list:
    # 检查文件扩展名是否为EDF
    if file_name.endswith('.npy'):
    # if file_name.startswith('10s_') and file_name.endswith('T3.npy'): 
        print(file_name)
        file_path = os.path.join(folder_path, file_name)
        print(file_path)
        data = np.load(file_path)
        labels = []
        for i in range(data.shape[0]):
            label = label_make(i, data[i], 512, 5)
            labels.append(label)
        labels = np.array(labels)
        print(labels)

        needmodify = False
        num0_str = input("是否需要修改数据(1需要/0不需要)")
        while not (num0_str.isdigit() and 0<=int(num0_str)<=1):
            num0_str = input("无效输入，请重新输入seq：")
        num0 = int(num0_str)

        if (num0 == 1):
            needmodify = True
        
        while (needmodify):
            num1_str = input("请输入seq：")
            while not num1_str.isdigit():
                num1_str = input("无效输入，请重新输入seq：")
            num1 = int(num1_str)
            num2_str = input("请输入epoch：")
            while not (num2_str.isdigit() and 1<=int(num2_str)<=5):
                num2_str = input("无效输入，请重新epoch：")
            num2 = int(num2_str)
            labels[num1-1][num2-1] = 1-labels[num1-1][num2-1]

            num3_str = input("修改是否结束(键入1(已结束)/0(未结束))?")
            if num3_str == '1':
                needmodify = False

        print(labels)
        time.sleep(0.3)
        save_path = os.path.join(s_path, file_name)
        print(save_path)
        print("一个文件处理完成----")
        np.save(save_path[:-4] + "_label.npy", labels)
        try:
            # 使用shutil.move()函数移动文件
            shutil.move(file_path, s_path)
            print("文件移动成功！")
        except FileNotFoundError:
            print("源文件不存在或路径错误。")
        except shutil.Error:
            print("文件移动失败。")
