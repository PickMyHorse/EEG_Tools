import numpy as np
import matplotlib.pyplot as plt
import os

fs = 256  # 频率

def plt_one_file(epoch, folder_path):
    file_list = os.listdir(folder_path)
    round = 0

    endings_mapping = {
        'C3.npy': 0,
        'C4.npy': 1,
        'F3.npy': 2,
        'F4.npy': 3,
        'O1.npy': 4,
        'O2.npy': 5,
        'T3.npy': 6,
        'T4.npy': 7
    }

    coordinates_mapping = {
        'C3_label.npy': 0,
        'C4_label.npy': 400,
        'F3_label.npy': 800,
        'F4_label.npy': 1200,
        'O1_label.npy': 1600,
        'O2_label.npy': 2000,
        'T3_label.npy': 2400,
        'T4_label.npy': 2800
    }

    for file_name in file_list:
        # 检查文件扩展名是否为EDF
        if file_name.endswith('.npy'):
            file_path = os.path.join(folder_path, file_name)
            data0 = np.load(file_path)
            amount = int((np.prod(data0.shape)) / fs / 2 / epoch)
            if (amount > round):
                round = amount

    for i in range(round):
        fig, ax = plt.subplots(figsize=(3 * epoch, 3 * 8))
        # x轴
        ax.set_xlim(0, epoch)
        # 设置时间轴
        time = np.linspace(0, epoch, num=epoch * fs * 2)
        x_ticks = range(0, epoch + 1, 1)
        ax.set_xticks(x_ticks)

        # y轴
        ax.set_ylim(0, 3200)
        y_positions = [200, 600, 1000, 1400, 1800, 2200, 2600, 3000]
        y_labels = ["C3", "C4", "F3", "F4", "O1", "O2", "T3", "T4"]
        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels, fontsize=80)  # y轴标记字体大小

        # 填充整个图像区域为天蓝色背景，此处可修改
        ax.fill_between([0, epoch], 0, 3200, color='skyblue')

        for file_name in file_list:
            # 检查文件扩展名是否为EDF
            if file_name.endswith('.npy'):
                file_path = os.path.join(folder_path, file_name)
                data = np.load(file_path)

                line_objects = {}
                for ending, idx in endings_mapping.items():
                    if file_name.endswith(ending):
                        newdata = data.flatten()[(i * (epoch * fs * 2)):((i + 1) * (epoch * fs * 2))]
                        line = ax.plot(time, newdata + 200 + 400 * idx, linewidth=2, color='black')  # eeg图像颜色，可修改
                        line_objects[idx] = line[0]  # 提取 Line2D 对象

                fill_objects = {}
                for ending, y_coord in coordinates_mapping.items():
                    if file_name.endswith(ending):
                        total_elements = 0
                        for row_idx in range(int(i * (epoch/5)), data.shape[0]):
                            row = data[row_idx]
                            for col_idx, val in enumerate(row):
                                if val == 1:
                                    x1, y1 = (row_idx-i*(epoch/5)) * 5 + col_idx, y_coord
                                    x2, y2 = x1 + 1, y1 + 400
                                    fill = ax.fill_between([x1, x2], y1, y2, color='orange', alpha=0.5)  # 坏段颜色
                                    fill_objects[(x1, y1, x2, y2)] = fill
                                total_elements += 1
                                if total_elements >= epoch:
                                    break

                            if total_elements >= epoch:
                                break

        save_path = os.path.join(folder_path, f"{i}_image.png")
        plt.savefig(save_path, dpi=200, bbox_inches=None)  # 保存图像分辨率

        for line in line_objects.values():
            line.remove()
        line_objects.clear()

        for fill in fill_objects.values():
            fill.remove()
        fill_objects.clear()

plt_one_file(20, "C:/Users/12944/Desktop/draw_graph/graph/")
