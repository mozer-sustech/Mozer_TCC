import numpy as np
import matplotlib.pyplot as plt

# 打开文件并读取所有行
with open("MD_TRAJECTORY.xyz-pos-1.xyz", "r") as f:
    lines = f.readlines()

# 获取帧数和原子数
atom_count = int(lines[0])
num_frames = len(lines) // (atom_count + 2)
print("总原子数目：%d"%atom_count)

# 用input函数让用户指定需要分析原子的原子序号
atom_num= input("请输入需要分析原子的原子序号：")
atom_index = int(atom_num) - 1

# 创建一个空的数组来存储坐标
coordinates = np.zeros((num_frames, atom_count, 3))

# 解析每一帧的坐标
for i in range(num_frames):
    # 获取该帧的起始行
    start_index = i * (atom_count + 2) + 2
    for j in range(atom_count):
        # 解析该原子的坐标
        line = lines[start_index + j]
        parts = line.split()
        symbol = parts[0]
        x, y, z = map(float, parts[1:])
        # 将坐标存储到数组中
        coordinates[i, j] = [x, y, z]

# 提取出该原子在所有帧下的空间坐标，并导入新建的txt文件
atom_coordinates = coordinates[:, atom_index, :]
np.savetxt("atom_%s_coordinates.txt"%atom_num, atom_coordinates)

# 将XYZ数据可视化 Time-XYZ Two-Dimension
fig, ax = plt.subplots(figsize=(8, 6))
time = np.arange(num_frames)
x = coordinates[:, atom_index, 0]
y = coordinates[:, atom_index, 1]
z = coordinates[:, atom_index, 2]
ax.plot(time, x, label='X')
ax.plot(time, y, label='Y')
ax.plot(time, z, label='Z')
ax.set_xlabel('Time')
ax.set_ylabel('Coordinate')
ax.legend()
plt.show()

# 将原子的运动轨迹可视化
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
x = coordinates[:, atom_index, 0]
y = coordinates[:, atom_index, 1]
z = coordinates[:, atom_index, 2]
ax.plot(x, y, z, lw=1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
