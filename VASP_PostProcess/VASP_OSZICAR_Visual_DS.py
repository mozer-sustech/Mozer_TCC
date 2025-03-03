import re
import pandas as pd
import matplotlib.pyplot as plt

def parse_oszicar(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            if 'T=' in line:
                # 提取时间步
                parts = line.split()
                step = int(parts[0])
                
                # 提取温度（第三个元素去掉末尾的.）
                temp = int(parts[2].rstrip('.'))
                
                # 提取所有物理量
                quantities = {}
                matches = re.findall(r'(\w+)= (-?[\d\.]+[Ee][+-]?\d+)', line)
                for key, value in matches:
                    quantities[key] = float(value)
                
                # 合并数据
                data.append({
                    'Step': step,
                    'Temperature': temp,
                    **quantities
                })
    
    return pd.DataFrame(data)

# 使用示例
df = parse_oszicar('OSZICAR')

# 写入Excel
df.to_excel('oszicar_analysis.xlsx', index=False)

# 可视化
fig, (ax1, ax2,ax3) = plt.subplots(3, 1, figsize=(10, 8))

# 温度图
ax1.plot(df['Step'], df['Temperature'], 'r-', label='Temperature')
ax1.set_ylabel('Temperature (K)')
ax1.legend()
# ax1.grid(True)

# 能量图（假设能量对应的键是'E'）
# if 'E' in df.columns:
ax2.plot(df['Step'], df['E'], 'b-', label='G')
ax2.set_ylabel('Free Energy (eV)')
ax2.legend()
# ax2.grid(True)

ax3.plot(df['Step'], df['E0'], 'b-', label='E0')
ax3.set_ylabel('Potential Energy (eV)')
ax3.legend()
# ax3.grid(True)

ax3.set_xlabel('Time Step')
plt.tight_layout()
plt.savefig('temperature_energy_plot.png')
plt.show()