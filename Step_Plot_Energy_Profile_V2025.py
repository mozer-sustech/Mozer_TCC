import pandas as pd
import matplotlib.pyplot as plt

# ======== 用户自定义区域 ========
path_colors = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd']  # 按列顺序为 A、B、C、D... 路径配色
show_full_frame = False       # False：仅显示左侧 Y 轴；True：显示四边框
dot_size = 50                 # 散点大小
label_fontsize = 8            # 能量值字体大小
step_fontsize = 9             # 步骤名字体大小
# ================================

# 1. 读取 Excel 文件
file_path = 'EnergyProfile.xlsx'  # 替换为你的文件名
df = pd.read_excel(file_path)

steps = df.iloc[:, 0].astype(str)     # 第一列：步骤名称
path_data = df.iloc[:, 1:]            # 后续列：各条路径的能量数据
num_steps = len(steps)

fig, ax = plt.subplots(figsize=(10, 6))

# 2. 绘制每条路径
for idx, col in enumerate(path_data.columns):
    energies = path_data[col].astype(float).values
    color = path_colors[idx % len(path_colors)]
    
    # 2.1 实线台阶
    for i, E in enumerate(energies):
        ax.hlines(E, i, i + 0.8, colors=color, linewidth=2)
    
    # 2.2 虚线连接
    for i in range(num_steps - 1):
        ax.plot([i + 0.8, i + 1], [energies[i], energies[i + 1]],
                linestyle='--', color=color, linewidth=1)
    
    # 2.3 标记点
    x_pts = [i + 0.4 for i in range(num_steps)]
    ax.scatter(x_pts, energies, color=color, s=dot_size, zorder=5, label=col)
    
    # 2.4 能量数值标签
    for i, E in enumerate(energies):
        ax.text(i + 0.4, E + 0.02, f"{E:.2f}", 
                ha='center', va='bottom', fontsize=label_fontsize, color='dimgray')

# 3. 步骤名称标签：居中显示在各台阶下方
ymin, ymax = ax.get_ylim()
for i, step in enumerate(steps):
    ax.text(i + 0.4, ymin - (ymax - ymin)*0.05, step,
            ha='center', va='top', fontsize=step_fontsize, color='black')

# 4. 坐标轴、图例与边框
ax.set_ylabel("Energy (eV)", fontsize=12)
ax.set_title("Catalytic Reaction Energy Profile — Multi Pathways", fontsize=14)
ax.set_xticks([])        # 隐藏 X 轴刻度
ax.legend(title="Pathways")
ax.grid(False)

# 边框控制
if show_full_frame:
    for spine in ax.spines.values():
        spine.set_visible(True)
else:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(True)

plt.tight_layout()
plt.show()
