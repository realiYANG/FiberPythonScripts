import os
import pandas as pd
import lasio
import re
from datetime import datetime


def parse_filename(filename):
    # 使用正则表达式匹配日期和时间
    match = re.search(r'(\d{6})(\d{6})', filename)
    if match:
        date_str, time_str = match.groups()
        # 格式化日期和时间
        date = datetime.strptime(date_str, '%y%m%d').date()
        time = datetime.strptime(time_str, '%H%M%S').time()
        # 合并日期和时间
        datetime_combined = datetime.combine(date, time)
        return datetime_combined
    else:
        print("Invalid format")
        return None


# 抽稀
las_folder = "E:\\华H39-5井IDAS_las数据\\开井" #TODO
files = os.listdir(las_folder)
selected_files = []  # 选中的文件列表
for i, file in enumerate(files):
    if file.endswith('.las') and i % 60 == 0:
        selected_files.append(file)

# 遍历文件夹下的所有文件
for filename in selected_files:
    # 读取LAS文件
    las = lasio.read(os.path.join(las_folder, filename))

    # 提取深度列和最后一列数据列
    depth = las['DEPT']
    data = las['SSTR']

    # 将numpy.ndarray数组转换为pandas序列对象
    depth = pd.Series(depth)
    data = pd.Series(data)

    # 将深度列和数据列合并为一个DataFrame
    df = pd.concat([depth, data], axis=1)

    # 将文件名的扩展名替换为CSV，并保存为CSV文件
    csv_filename = os.path.splitext(filename)[0] + '.csv'
    print(csv_filename)
    filename = csv_filename
    datetime_combined = parse_filename(filename)
    print(datetime_combined)

    # 修改第一行的内容
    df.columns = ['Depth', str(datetime_combined)]

    # 保存修改后的结果
    df.to_csv(os.path.join(las_folder, csv_filename), index=False)

print("dts转csv完成！")

# 拼接————————————————————————————————————————————————————————————————————
folder_path = las_folder
folder_path_last = folder_path.split("\\")[-1]

# 获取文件夹中所有CSV文件的文件名
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
# 创建一个空的DataFrame，用于存储拼接后的数据
combined_csv = pd.DataFrame()
# 循环读取并拼接所有CSV文件
for i, csv_file in enumerate(csv_files):
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    if combined_csv.empty:
        combined_csv = df
    else:
        combined_csv = pd.concat([combined_csv, df.iloc[:, 1:]], axis=1)
# 将拼接后的数据保存为新的CSV文件
output_path = os.path.join(os.getcwd(), folder_path_last + '_combined_csv.csv')
combined_csv.to_csv(output_path, index=False)
print("拼接完成！")
