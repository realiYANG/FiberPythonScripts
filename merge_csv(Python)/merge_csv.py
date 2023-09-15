import os
import pandas as pd

# 替换为您的CSV文件所在的文件夹路径
folder_path = "path/to/your/csv/folder"

# 获取文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# 初始化一个空的DataFrame
merged_df = None

for csv_file in csv_files:
    # 读取CSV文件
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)

    if merged_df is None:
        # 如果是第一个CSV文件，则直接将其设置为merged_df
        merged_df = df
    else:
        # 否则，将新的CSV文件与merged_df合并
        # 注意，这假设所有CSV文件的第一列是相同的，因此只从第二列开始合并
        merged_df = pd.concat([merged_df, df.iloc[:, 1:]], axis=1)

# 将合并后的DataFrame保存为一个新的CSV文件
merged_df.to_csv("merged.csv", index=False)