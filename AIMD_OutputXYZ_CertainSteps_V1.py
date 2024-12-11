import os

print("To Seperate the AIMD Trajectory")
print("Get Output Structure of XYZ in Certain Steps")
print("Writen By WeiCAO in 2023.05.29")

# 打开轨迹文件
file_name = "MD_TRAJECTORY.xyz-pos-1.xyz"
with open(file_name, "r") as trajectory_file:
    lines = trajectory_file.readlines()

# 获取原子数目
num_atoms = int(lines[0])

# 获取用户输入的间隔数
X = int(input("请输入间隔数 X："))

#
for i in range(1, len(lines), num_atoms + 2):
    frame_number = int(lines[i].split("=")[1].split(",")[0])
    if frame_number % X == 0:
        filename = f"MD_{frame_number}.xyz"
        with open(filename, "w") as output_file:
            output_file.write("".join(lines[i-1 : i +num_atoms+1 ]))

print("Enter to Exit")