# 用来将silixa采集软件输出的las格式的DTS/DAS数据转换为Therma可加载的csv格式
# 输入： las格式的DTS/DAS的文件夹
# 输出：Temperature、RMS
# V1.0 coder: zhangbeibei


import lasio
import os
import pandas as pd
import os
import sys


def dts(dir, csv_dir):
    df_temp_baseline = pd.DataFrame()
    df_temp_fast = pd.DataFrame()
    df_temp_slow = pd.DataFrame()

    count = 0
    # for file in list(os.walk(dir))[0][2]:
    for filepath, dirname, filenames in os.walk(dir):
        for filename in filenames:
            abs_path = os.path.join(filepath, filename)
            if filename.split(".")[-1] != "las":
                continue
            # if filename.split(".")[0][-2:] != "00":
            #     continue
            print("reading %s..." % abs_path)
            las = lasio.read(abs_path)
            ts = filename.split("_")[-1].split(".")[0]
            year = "20" + ts[0:2]
            month = ts[2:4]
            day = ts[4:6]
            hour = ts[6:8]
            minute = ts[8:10]
            second = ts[10:12]
            timestamp = "%2s/%2s/%4s %2s:%2s:%2s" % (
                day, month, year, hour, minute, second)

            if count == 0:
                df_temp_baseline["depth"] = las["DEPT"]
                df_temp_fast["depth"] = las["DEPT"]
                try:
                    df_temp_slow["depth"] = las["DEPT"]
                except:
                    pass

            # df_temp_baseline[timestamp] = las["TEMP:1"]
            # df_temp_fast[timestamp] = las["TEMP:2"]
            df_temp_baseline = pd.concat([df_temp_baseline, pd.DataFrame(columns=[timestamp], data=las["TEMP:1"])],
                                         axis=1)
            df_temp_fast = pd.concat([df_temp_fast, pd.DataFrame(columns=[timestamp], data=las["TEMP:2"])], axis=1)
            try:
                # df_temp_slow[timestamp] = las["TEMP:3"]
                df_temp_slow = pd.concat([df_temp_slow, pd.DataFrame(columns=[timestamp], data=las["TEMP:3"])], axis=1)
            except:
                pass

        df_temp_baseline.to_csv(os.path.join(csv_dir, "DTS_baseline.csv"), index=False)
        df_temp_fast.to_csv(os.path.join(csv_dir, "DTS_fast.csv"), index=False)
        try:
            df_temp_fast.to_csv(os.path.join(csv_dir, "DTS_slow.csv"), index=False)
        except:
            pass

        for dts in ["DTS_baseline", "DTS_fast"]:
            with open(os.path.join(csv_dir, dts + ".csv"), "r") as f:
                content = f.read()
            with open(os.path.join(csv_dir, dts + ".csv"), "w") as f1:
                f1.write("Depth [m],%s [degC]\n" % dts + content[5:])

        try:
            with open(os.path.join(csv_dir, "DTS_slow.csv"), "r") as f:
                content = f.read()
            with open(os.path.join(csv_dir, "DTS_slow.csv"), "w") as f1:
                f1.write("Depth [m],DTS_slow [degC]\n" + content[5:])
        except:
            pass


def das(dir, csv_dir):
    createVar = locals()
    i = 0
    for i in range(count_freq):
        createVar['df_das_' + str(i)] = pd.DataFrame()
    df_das_sstr = pd.DataFrame()

    count = 0
    for filepath, dirname, filenames in os.walk(dir):
        for filename in filenames:
            abs_path = os.path.join(filepath, filename)
            if filename.split(".")[-1] != "las":
                continue
            # if filename.split(".")[0][-2:] != "00":
            #     continue

            print("reading %s..." % abs_path)
            las = lasio.read(abs_path)
            ts = filename.split("_")[-1].split(".")[0]
            year = "20" + ts[0:2]
            month = ts[2:4]
            day = ts[4:6]
            hour = ts[6:8]
            minute = ts[8:10]
            second = ts[10:12]
            timestamp = "%2s/%2s/%4s %2s:%2s:%2s" % (
                day, month, year, hour, minute, second)

            if count == 0:
                i = 0
                for i in range(count_freq):
                    createVar['df_das_' + str(i)]["depth"] = las["DEPT"]
                try:
                    df_das_sstr["depth"] = las["DEPT"]
                except:
                    pass

            i = 0
            for i in range(count_freq):
                RMS_name = ''.join(['RMS[', str(i), ']'])
                createVar['df_das_' + str(i)] = pd.concat([createVar['df_das_' + str(i)], pd.DataFrame(columns=[timestamp], data=las[RMS_name])], axis=1)
            try:
                df_das_sstr = pd.concat([df_das_sstr, pd.DataFrame(columns=[timestamp], data=las["SSTR"])], axis=1)
            except:
                pass

            count += 1

        i = 0
        for i in range(count_freq):
            FBE_name = ''.join(['FBE', str(i), '.csv'])
            createVar['df_das_' + str(i)].to_csv(os.path.join(csv_dir, FBE_name), index=False)
        try:
            df_das_sstr.to_csv(os.path.join(csv_dir, "SSTR.csv"), index=False)
        except:
            pass

        # 初始化数组
        FBE = []

        # 频率范围字典构建
        for i in range(count_freq):
            FBE_name = ''.join(['FBE', str(i)])
            FBE.append(FBE_name)
        FBE.append('SSTR')
        print(FBE)

        for das in FBE:
            with open(os.path.join(csv_dir, das + ".csv"), "r") as f:
                content = f.read()
            with open(os.path.join(csv_dir, das + ".csv"), "w") as f1:
                f1.write("Depth [m],%s [unitless]\n" % das + content[5:])


if __name__ == "__main__":
    # type = int(input("dts:0, das:1\n"))
    type = 0
    # dir = r"C:\Users\Administrator\Desktop\input"
    # dir = input("las输入文件目录,然后回车即可:\n")
    # csv_dir = r"C:\Users\Administrator\Desktop\input\1"
    # csv_dir = os.path.dirname(sys.executable)
    #   if type == 0:
    #       dts(dir, csv_dir)
    #   else:

    dir_workspace = input("输入工区目录,然后回车即可:\n")
    dir_las = dir_workspace + '\\0las\\'
    dir_csv = dir_workspace + '\\1csv\\'
    dir_dts = dir_workspace + '\\2dts\\'

    las_file = [f for f in os.listdir(dir_las) if f.endswith('.las')]
    las = lasio.read(dir_las + las_file[0])
    data = las.curves

    # 判断有多少组频率
    global count_freq
    count_freq = len(data) - 2

    das(dir_las, dir_csv)
    # input("回车结束运行\n")
