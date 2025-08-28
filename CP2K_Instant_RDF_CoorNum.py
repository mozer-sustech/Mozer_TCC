import matplotlib.pyplot as plt

def distance(x, y):
    return ((x[0] - y[0])**2 + (x[1] - y[1])**2 + (x[2] - y[2])**2)**0.5

def count_elements_around_center(md_file, center, element, cut_num):
    data = {"frame": [], "count": []}
    with open(md_file, "r") as f:
        lines = f.readlines()

    num_atoms = int(lines[0].strip())
    num_frames = len(lines) // (num_atoms + 2)

    for i in range(num_frames):
        frame_start = i * (num_atoms + 2) + 2
        frame_end = frame_start + num_atoms

        center_coords = [float(coord) for coord in lines[frame_start + center].split()[1:]]
        element_count = 0

        for j in range(num_atoms):
            if j == center:
                continue

            atom_coords = [float(coord) for coord in lines[frame_start + j].split()[1:]]
            if distance(center_coords, atom_coords) <= cut_num:
                if lines[frame_start + j].split()[0] == element:
                    element_count += 1

        data["frame"].append(i)
        data["count"].append(element_count)

    return data

def plot_data(data, element):
    plt.plot(data["frame"], data["count"], marker='o')
    plt.xlabel('Frame Number')
    plt.ylabel(f'{element} Count around Center Atom')
    plt.title(f'{element} Count around Center Atom vs Frame Number')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    md_file = "MD_TRAJECTORY.xyz-pos-1.xyz"

    # 用户输入Center原子序号、Element元素符号和Cut_Num截断距离
    center = int(input("请输入Center原子序号（从0开始）："))
    element = input("请输入Element元素符号：")
    cut_num = float(input("请输入Cut_Num截断距离："))

    data = count_elements_around_center(md_file, center, element, cut_num)
    plot_data(data, element)
