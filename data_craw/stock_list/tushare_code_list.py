import tushare as ts
import json
import pandas as pd

class CodeList(object):

    def __init__(self, save_path="E:\\files\\stock\\code_list.csv"):
        f = open("const.json", "r", encoding="utf8")
        consts = json.loads(f.read())
        self.save_path = save_path
        self.pro = ts.pro_api(consts['tushare']['token'])       # 初始化 tushare 接口
        self.list = None
    
    def get_list(self):
        self.list = data = self.pro.stock_basic(
            exchange='', 
            list_status='L', 
            fields='''
                ts_code,
                symbol,
                name,
                area,
                industry,
                market,
                exchange,
                curr_type,
                list_date
            '''
        )

    def save_to_csv(self):
        self.list.columns = [
            'ts_code',      # ts_code => tushare 的代码
            '股票代码',      # symbol  => 股票代码
            '名称',          # name => 股票名称
            '所在地域',       # area
            '所属行业',       # industry
            '市场类型',       # market => 市场类型 （主板/中小板/创业板）
            '交易所代码',     # exchange
            '交易货币',       # curr_type
            '上市日期'        # list_date
        ]
        for index, row in self.list.iterrows():
            row['股票代码'] = "`" + row['股票代码']
        self.list.to_csv(self.save_path, sep=',', header=True, index=False, encoding="gbk")

    
if __name__ == "__main__":
    cl = CodeList()
    cl.get_list()
    cl.save_to_csv()