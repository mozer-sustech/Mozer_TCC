##For transformation of .car file to .xyz file
##Writen by Wei CAO, 20230205##
##Supported by ChatGPT##

import os

# 遍历当前文件夹下所有后缀名为car的文件
for file in os.listdir():
    if file.endswith(".car"):
        # 打开输入文件，读取每一行，并判断是否满足条件
        with open(file, "r") as f:
            lines = f.readlines()
            new_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) == 9:
                    new_line = " ".join(elements)
                    new_lines.append(new_line)

        # 保留第2、3、4、8列的数据，并将其写入新文件
        new_file_name = os.path.splitext(file)[0] + ".xyz"
        with open(new_file_name, "w") as f:
            # 写入新文件的前两行
            f.write(str(len(new_lines)) + "\n")
            f.write(new_file_name + "\n")

            # 写入保留的数据
            for line in new_lines:
                elements = line.split()
                new_elements = [elements[7], elements[2], elements[3], elements[1]]
                new_line = "\t".join(new_elements)
                f.write(new_line + "\n")

        print(f"文件{file}已成功处理并转换为{new_file_name}。")
