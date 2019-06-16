import os
import pandas as pd
from tqdm import tqdm


class MA(object):

    def __init__(self, day_line_file_prefix, end_date="0000-00-00"):
        self.day_line_file_prefix = day_line_file_prefix
        self.end_date = end_date

    # 计算单只股票的 ma_n
    def calculate_one_man(self, code, ma_n):
        try:
            df = pd.read_csv(self.day_line_file_prefix + str(code) + ".csv", encoding="gbk")
        except:
            print("文件%s.csv打开失败" % code)
            return False
        
        column_name = "MA" + str(ma_n)
        try:
            col = df[column_name]       # 已经存在该列
            return
        except:
            pass

        df[column_name] = ""

        start = 0
        block = df[start:start+ma_n]
        if len(block) < ma_n or block.values[0][0] < self.end_date:
            return
        