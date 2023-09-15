# coding=utf-8
import lasio
import os

import pandas as pd

#############说明##############
#本程序是为了把Silixa公司的DAS数据转换成Ariane可导入的dts数据格式
#需要原始的las文件和已解析好的csv文件
#首先解析las文件头获取频率范围，然后将csv文件转换成dts文件（本质上是一种las格式）

def DAS_csv2dts(dir_csv, dir_las):
    list_csv = []
    for file in list(os.walk(dir_csv))[0][2]:
        if file.split(".")[-1] == "csv":
            list_csv.append(file)

    df_list = {}
    for i in list_csv:
        df = pd.read_csv(os.path.join(dir_csv, i), skiprows=[0])
        df.columns = ["DEPT"] + list(df.columns)[1:]
        fbno = i.split(".")[0]
        df_list[fbno] = df
        column = list(df.columns)
        dept = list(df["DEPT"])

    for co in column:
        las = lasio.LASFile()
        if co == "DEPT":
            continue

        las.append_curve("DEPTH", dept, unit="m", descr="Depth curve")
        for m in df_list.keys():
            if m == "SSTR":
                las.append_curve("SSTR", df_list[m][co], unit="NM/M/S", descr="SLOW STRAIN RATE")
                continue
            no = m.replace("FBE", "")
            desc = "Sonic energy in frequency band{:>10.1f} to{:>10.1f} (Hz)".format(FB[m][0], FB[m][1])
            las.append_curve("DAS_EN0%s" % no, df_list[m][co], unit="Unity".format(no), descr=desc)

        # timestamp = "13/07/2023 13:00:00"
        year = co[6:10]
        month = co[3:5]
        day = co[0:2]
        hour = co[11:13]
        minute = co[14:16]
        second = co[17:]
        las.well.TIMESTAMP = lasio.HeaderItem(mnemonic="TIMESTAMP", descr="%4s/%2s/%2s %2s/%2s/%2s" % (
            year, month, day, hour, minute, second))
        las_name = "DAS_1_%4s-%2s-%2sT%2s-%2s-%2s.dts" % (year, month, day, hour, minute, second)
        las.write(os.path.join(dir_las, las_name))
        print(las_name)


if __name__ == "__main__":

    # csv文件目录
    dir_workspace = input("输入工区目录,然后回车即可:\n")
    dir_las = dir_workspace + '\\0las\\'
    dir_csv = dir_workspace + '\\1csv\\'
    dir_dts = dir_workspace + '\\2dts\\'
    las_file = [f for f in os.listdir(dir_las) if f.endswith('.las')]
    las = lasio.read(dir_las + las_file[0])
    data = las.curves

    # 判断有多少组频率
    count_freq = len(data) - 2

    # 初始化字典
    FB = {}

    # 频率范围字典构建
    for i in range(count_freq):
        FBE_name = ''.join(['FBE', str(i)])
        FB[FBE_name] = [int(data[i + 1].descr.split("Hz")[0].split(" ")[-2]),
                        int(data[i + 1].descr.split("Hz")[1].split(" ")[-2])]
    FB["SSTR"] = ["SLOW STRAIN RATE"]
    print(FB)

    # dts文件目录
    dts_dir = dir_workspace + '\\2dts'
    if not os.path.exists(dts_dir):
        os.mkdir(dts_dir)
    DAS_csv2dts(dir_csv, dts_dir)
