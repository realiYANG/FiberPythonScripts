import os
import pandas as pd
# 选择要拼接的CSV文件夹
#folder_path = input("请输入DTS文件夹路径,然后回车即可:\n")
folder_path = "C:\\Users\\kiwifruitlove123\\Desktop\\dts_csv\\09_60min"
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