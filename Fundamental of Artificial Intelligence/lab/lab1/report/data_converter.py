import os


all_output_files = os.listdir("../digit/output/")
for file in all_output_files:
    print("-" * 20)
    print(file[7:-4])
    print("-" * 20)
    case_num = 0
    path = ""
    time = 0
    step_num = 0
    print("\\hline")
    print("样例编号 & 运行时间/s & 移动序列 & 总步数 \\\\")
    print("\\hline")
    with open("../digit/output/" + file, "r") as f:
        datas = f.readlines()
        for data in datas:
            data = data.strip().split(",")
            print(f"{case_num:02d} & {data[1]} & {data[0]} & {len(data[0])}  \\\\")
            case_num += 1
    print("\\hline")
    print("-" * 20)
    print()
