import matplotlib.pyplot as plt

# 定义文件名
file_name = "MD_ENERGY-1.ener"

# 初始化存储数据的列表
time = []
kinetic_energy = []
temperature = []
potential_energy = []
conserved_energy = []
step_time = []

# 读取文件并解析数据
try:
    with open(file_name, 'r') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"文件 {file_name} 未找到，请确保它在当前目录下。")
    exit()

for line in lines:
    if line.strip() and not line.startswith('#'):  # 跳过空行和注释行
        columns = line.split()
        try:
            time.append(float(columns[1]))  # 时间（第2列）
            kinetic_energy.append(float(columns[2]))  # 动能（第3列）
            temperature.append(float(columns[3]))  # 温度（第4列）
            potential_energy.append(float(columns[4]))  # 势能（第5列）
            conserved_energy.append(float(columns[5]))  # 守恒能量（第6列）
            step_time.append(float(columns[6]))  # 每步耗时（第7列）
        except IndexError:
            print(f"数据格式不正确，请检查文件内容：{line.strip()}")
            exit()

# 创建组图
fig, axes = plt.subplots(5, 1, figsize=(10, 15), sharex=True)
fig.suptitle('AIMD Data Analysis', fontsize=16)

# 定义子图内容
titles = ['Kinetic Energy (a.u.)', 'Temperature (K)', 'Potential Energy (a.u.)', 
          'Conserved Energy (a.u.)', 'Step Time (fs)']
y_data = [kinetic_energy, temperature, potential_energy, conserved_energy, step_time]
colors = ['blue', 'green', 'red', 'purple', 'orange']

# 绘制每个子图
for i, ax in enumerate(axes):
    ax.plot(time, y_data[i], color=colors[i], linestyle='-', linewidth=1.5, marker='o', markersize=3)
    ax.set_ylabel(titles[i], fontsize=12)
    ax.grid(True)
    ax.set_title(titles[i], fontsize=14)

# 设置共享的 X 轴标签
axes[-1].set_xlabel('Time (fs)', fontsize=14)

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
