import os
import pandas as pd
from tqdm import tqdm
import json
import threading
import math

class MA(object):

    def __init__(self, day_line_file_prefix, n_arr=[5, 10, 20, 30, 60], end_date="0000-00-00"):
        self.day_line_file_prefix = day_line_file_prefix
        self.end_date = end_date
        self.n_arr = n_arr

    # 计算单只股票的 ma_n
    def calculate_one_ma_n(self, code, n):
        try:
            df = pd.read_csv(self.day_line_file_prefix + str(code) + ".csv", encoding="gbk")
        except:
            print("文件%s.csv打开失败" % code)
            return False
        
        column_name = "MA" + str(n)
        try:
            col = df[column_name]       # 已经存在该列
            return
        except:
            pass

        df[column_name] = ""

        sum_of_block = 0
        block = df[0:n]
        if len(block) < n or block.values[0][1] < self.end_date:
            return
        for index, row in block.iterrows():
            sum_of_block += row['收盘价']
        for index, row in df.iterrows():
            if index != 0:  
                try:
                    sum_of_block = sum_of_block - df.loc[index-1, "收盘价"] + df.loc[index+n-1, "收盘价"]
                except:
                    break
                if row['日期'] < self.end_date:
                    break 
            ma = sum_of_block / n
            df.loc[index, column_name] = ma

        df.to_csv(self.day_line_file_prefix + str(code) + ".csv", index=False, encoding="gbk")

    def calculate_block(self, block):
        for i in tqdm(range(len(block))):
            code = block[i]
            for n in self.n_arr:
                self.calculate_one_ma_n(code, n)

    def calculate_by_threads(self, thread_num):
        file_list = os.listdir(self.day_line_file_prefix)
        codes = []
        for file in file_list:
            codes.append(file[0:6])
        all_count = len(codes)
        offset = math.ceil(all_count / thread_num)
        threads = []
        for i in range(thread_num):
            start = i * offset
            end = (i+1)*offset if (i+1)*offset < all_count else all_count
            block = codes[start:end]
            thread = threading.Thread(target=self.calculate_block, args=(block, ))
            threads.append(thread)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

    def check(self):
        file_list = os.listdir(self.day_line_file_prefix)
        codes = []
        for i in tqdm(range(len(file_list))):
            filename = file_list[i]
            code = filename[0:6]
            try:
                df = pd.read_csv(self.day_line_file_prefix + code + ".csv", encoding="gbk")
            except:
                print("%s.csv打开失败" % code)
            try:
                for n in self.n_arr:
                    column_name = "MA%s" % n
                    col = df[column_name]
            except:
                codes.append(code)
        for code in codes:
            print(code)

if __name__ == "__main__":
    f = open("const.json", "r", encoding='utf8')
    consts = json.loads(f.read())
    day_line_file_prefix = consts["day_line_file_prefix"]
    ma = MA(day_line_file_prefix, end_date="2016-01-01")
    # ma.calculate_one_ma_n("000001", 5)
    ma.calculate_by_threads(8)
    # ma.check()