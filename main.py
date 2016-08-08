#coding=utf-8

import os
import csv
import utils
from settings import settings

'''
该程序用于批量处理负荷数据，
可将负荷数据表进行归一化，
并将归一化数据拆分成有功/无功两个csv文件
用于构建openDSS的loadshape模型

已知问题：
目前要求原始数据必须为xls或xlsx
输出的格式必为csv
每个xls文件暂时只能有一个表，
若有多个表，选取的列标题不能一致，否则会有bug

使用前请配置settings.py文件
'''

project_path = settings['project_path']
data_path = settings['data_path']
sheets = settings['sheets']
index = settings['sheets_index']
col_names = settings['col_names']
date_col = settings['date_col']
date = settings['date']
time_interval = settings['time_interval']

def process_csv(file, path):
    pass

def process_xls(file, path):
    file_path = os.path.join(path, file)
    print("正在处理%s" % file_path)
    tables = utils.get_xls_tables(file_path, sheets, index)
    cols = utils.get_table_column(tables, date_col, col_names)
    for task in [utils.max_column_data,
                 utils.fix_time_interval,
                 utils.check_missing_data,
                 utils.standardize_col_data]:
        cols = task(cols, date_col)
    return cols

def output(cols, path, filename):
    utils.cols_to_csv(cols, path, filename)
    pass

def batch_standardize_data(project_path, data_path):
    utils.check_os()
    utils.clear_log(date)
    path = os.path.join(project_path, data_path)
    all_file_list = utils.read_recursive_dir(path)
    for file_dict in all_file_list:
        for file in file_dict['file_list']:
            if utils.check_ext(file, ['.xls', '.xlsx']):
                cols = process_xls(file, file_dict['path'])
            # elif utils.check_ext(file, ['.csv', '.CSV']):
            #     cols = process_csv(file, file_dict['path'])
            else:
                continue
            utils.select_data_period(cols, date_col, date, time_interval)
            output(cols, file_dict['path'], file)

if __name__ == '__main__':
    batch_standardize_data(project_path, data_path)
    print("所有文件处理完成，处理结果保存在data.log文件中，可用记事本打开")
    os.system('pause')
