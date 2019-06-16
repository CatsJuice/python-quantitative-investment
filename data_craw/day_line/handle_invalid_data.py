import json
import os
import pandas as pd
from tqdm import tqdm
import math
import threading

f = open("const.json", "r", encoding='utf8')
consts = json.loads(f.read())

global DAY_LINE_FILE_PREFIX
DAY_LINE_FILE_PREFIX = consts['day_line_file_prefix']
global FILE_LIST
FILE_LIST = os.listdir(DAY_LINE_FILE_PREFIX)

def create_threds(thread_num):
    all_count = len(FILE_LIST)
    offset = math.ceil(all_count / thread_num)
    threads = []
    for i in range(thread_num):
        start = i * offset
        end = (i+1) * offset if (i+1)*offset < all_count else -1
        thread = threading.Thread(target=handle_block, args=(start, end, i))
        threads.append(thread)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

def handle_block(start, end, thread_id):
    global DAY_LINE_FILE_PREFIX
    global FILE_LIST
    block = FILE_LIST[start:end] if end > 0 else FILE_LIST[start:]
    for i in tqdm(range(len(block))):
        file_name = block[i]
        try:
            df = pd.read_csv(DAY_LINE_FILE_PREFIX + file_name, encoding="gbk")
        except:
            print("ERROR OPENING FILE: %s" % (DAY_LINE_FILE_PREFIX + file_name))
        drop_index = []
        for index, row in df.iterrows():
            if row['最高价'] == "None" or row['最高价'] == 0 \
                or row['最低价'] == "None" or row['最低价'] == 0 \
                or row['收盘价'] == "None" or row['收盘价'] == 0:
                drop_index.append(index)
        df = df.drop(drop_index)
        df.to_csv(DAY_LINE_FILE_PREFIX + file_name, encoding="gbk")

if __name__ == "__main__":
    
    
    create_threds(4)
    print("\nEND")