import csv
import os

# 定义要处理的目录路径
dir_path = "C:\\Users\\kiwifruitlove123\\Desktop\\DTS-Combine"

# 遍历目录下的所有文件
for filename in os.listdir(dir_path):
    # 确保只处理csv文件
    if filename.endswith(".csv"):
        # 构造输入和输出文件路径
        input_path = os.path.join(dir_path, filename)
        output_path = os.path.join(dir_path, "utf8_" + filename)

        # 打开输入文件并指定编码格式
        with open(input_path, "r", encoding="utf-8-sig") as input_file:
            # 读取csv数据
            csv_reader = csv.reader(input_file)

            # 打开输出文件并指定编码格式
            with open(output_path, "w", encoding="utf-8-sig", newline="") as output_file:
                # 写入csv数据
                csv_writer = csv.writer(output_file)
                csv_writer.writerows(csv_reader)

        # 删除原始文件
        os.remove(input_path)

        # 重命名输出文件为原始文件名
        os.rename(output_path, input_path)