#coding=utf-8

import os
import re
import csv
import xlrd
import datetime

'''
检查系统
若不为windows则直接中断程序
'''
def check_os():
    if os.name is "posix":
        raise TypeError("不支持该操作系统,请谨慎使用")
    else:
        print("正在初始化")

'''
处理列的标题，仅保留中文
去除其他所有符号和英文
'''
def strip_symbol(name):
    pattern = re.compile("[^\u4e00-\u9fa5]+")
    return pattern.sub("", name)

'''
将数据表里的时间数据
格式化为datetime对象
'''
def str_to_datetime(timestr):
    return datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

def str_to_time(timestr):
    unit = timestr[-1]
    if unit == 'h':
        return int(timestr[0:-1]) * 3600
    elif unit == 'm':
        return int(timestr[0:-1]) * 60
    elif unit == 'd':
        return int(timestr[0:-1]) * 86400

def datetime_to_str(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

def date_to_datetime(date):
    return datetime.datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d")

'''
清空log
'''
def clear_log(date):
    f = open("data.log", 'w')
    print('清空log日志...')
    f.write("数据日期:%s\n" % date)
    f.close()

'''
创建日志文件data.log
保存csv文件的输出路径
以及该csv文件的最大有名值
方便手工构建loadshape
'''
def write_log(desc, npts, type, max):
    f = open("data.log", 'a')
    f.write("%s npts=%d max-k%s=%g\n" % (desc, npts, type, max))
    f.close

'''
excel数据全部为字符串储存时
判断一个数据是否为数字
也可用正则实现
'''
def isnum(data):
    try:
        num = float(data)
    except ValueError:
        return False
    return True

'''
ext传入字符串或字符串list，代表期望的扩展名
若文件后缀名在ext的范围中，则返回True
'''
def check_ext(filename, ext):
    if type(ext) is str:
        ext = [ext]
    file_ext = os.path.splitext(filename)[1]
    return file_ext in ext

'''
输入项目名称和文件夹名，
将自动在当前目录下寻找该项目
并读取对应目录下的所有文件
'''
def read_dir(path):
    if os.path.isdir(path):
        file_list = os.listdir(path)
        return {'file_list': file_list, 'path': path}
    else:
        raise TypeError("not a directory")

'''
递归读取目录下所有的子文件夹内容
'''
def read_recursive_dir(path):
    all_file_list = []
    dir_dict = read_dir(path)
    dir_path = dir_dict['path']
    all_file_list.append(dir_dict)
    for file in dir_dict['file_list']:
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            file_list = read_recursive_dir(file_path)
            all_file_list.extend(file_list)
    return all_file_list

'''
读取csv文件
并将数据转换成list返回
暂时无用
'''
def get_csv_list(csv_path):
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file)
        csv_list = list(reader)
    return csv_list

'''
获取xls文件的对应表单
若sheets和index都不传则默认读第一张表
sheets传入表名组成的list对象
index传入索引组成dlist对象
不传则默认读取全部表
'''
def get_xls_tables(xls_path, sheets=[], index=[]):
    xls_file = xlrd.open_workbook(xls_path)
    tables = {}
    if not sheets and not index:
        table = xls_file.sheet_by_index(0)
        tables[table.name] = table
    else:
        for name in sheets:
            try:
                i = xls_file.sheet_names().index(name)
            except ValueError:
                continue
            index.append(i)
        # 去除重复
        index = set(index)
        for i in index:
            table = xls_file.sheet_by_index(i)
            tables[table.name] = table
    return (tables, xls_path)

'''
暂时无用
'''
def get_csv_column(csv_list, col_names=[]):
    cols = {}
    if col_names:
        for n in col_names:
            if n in csv_list[0]:
                index = csv_list[0].index(n)
                tmp_list = [row[index] for row in csv_list]
                cols[n] = {'list': tmp_list, 'index': index}
    else:
        index = 0
        tmp_list = [row[0] for row in csv_list]
        cols[0] = {'list': tmp_list, 'index': index}
    return cols

'''
若不传col_name参数则输出所有列的数据
'''
def get_table_column(tables, date_col, col_names=[]):
    file_name = tables[1]
    tables = tables[0]
    cols = {}
    if col_names:
        if date_col:
            col_names.append(date_col)
        for n in col_names:
            for table_name in tables:
                t = tables[table_name]
                if n in t.row_values(0):
                    index = t.row_values(0).index(n)
                    tmp_list = t.col_values(index)[1:]
                    cols[strip_symbol(n)] = {'list': tmp_list,
                                             'index': index,
                                             'table_name': table_name,
                                             'list_name': n,
                                             'file': file_name,
                                             'npts': len(tmp_list)}
    else:
        for table_name in tables:
            t = tables[table_name]
            for n in t.row_values(0):
                i = t.row_values(0).index(n)
                tmp_list = t.col_values(i)[1:]
                cols[strip_symbol(n)] = {'list': tmp_list,
                                         'index': i,
                                         'table_name': table_name,
                                         'list_name': n,
                                         'file': file_name,
                                         'npts': len(tmp_list)}
    return cols

'''
暂时无用
'''
def read_csv_len(csv_list=None, csv_path=None):
    if csv_list:
        return len(csv_list)
    elif csv_path:
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file)
            csv_list = list(reader)
        return len(csv_list)
    else:
        raise TypeError("两个参数至少有一个不为空")

'''
数据有不整齐，
某些数据采集间隔为1h,30m,15m不等
此函数将时间间隔统一化为15m
缺失点用其他时间点数据填补
多余点忽略
'''
def fix_time_interval(cols, date_col):
    delta = str_to_datetime(cols[date_col]['list'][0]) - str_to_datetime(cols[date_col]['list'][1])
    # 判断时间的升降序
    if delta.total_seconds() > 0:
        order = 'desc'
    else:
        order = 'asc'
    # 得到时间点的范围
    date_range = set()
    for d in cols[date_col]['list']:
        fd = str_to_datetime(d)
        date_range.add(date_to_datetime(fd.date()))
    date_range = list(date_range)
    date_range.sort()
    maxt = date_range[-1] + datetime.timedelta(0, 85500)
    mint = date_range[0]
    total_pts = int((maxt - mint) / datetime.timedelta(0, 900))
    for i in range(total_pts):
        delta = datetime.timedelta(0, 900*i)
        if order == 'desc':
            time_pt = datetime_to_str(maxt - delta)
            if i >= len(cols[date_col]['list']):
                cols[date_col]['list'].insert(i, time_pt)
                for col_name in cols:
                    if col_name != date_col:
                        cols[col_name]['list'].insert(i, "")
            if cols[date_col]['list'][i] != time_pt:
                cols[date_col]['list'].insert(i, time_pt)
                for col_name in cols:
                    if col_name != date_col:
                        cols[col_name]['list'].insert(i, "")
        elif order == 'asc':
            time_pt = datetime_to_str(mint + delta)
            if i >= len(cols[date_col]['list']):
                cols[date_col]['list'].insert(i, time_pt)
                for col_name in cols:
                    if col_name != date_col:
                        cols[col_name]['list'].insert(i, "")
            if cols[date_col]['list'][i] != time_pt:
                cols[date_col]['list'].insert(i, time_pt)
                for col_name in cols:
                    if col_name != date_col:
                        cols[col_name]['list'].insert(i, "")
    return cols

'''
检查原数据完整性
首尾数据若有缺失，用最邻近点的数据补足
中间数据若有缺失，用前后的数据取平均
'''
def check_missing_data(cols, date_col):
    for col_name in cols:
        if col_name == date_col:
            continue
        col_list = cols[col_name]['list']
        if col_list[-1] == '':
            i = -1
            while col_list[i-1] == '':
                i -= 1
            col_list[-1] = col_list[i-1]
        for k,n in enumerate(col_list):
            if n == "":
                if k == 0:
                    i = k
                    while col_list[i+1] == '':
                        i += 1
                    col_list[k] = col_list[i+1]
                else:
                    i = k
                    prev = col_list[k-1]
                    while col_list[i+1] == '':
                        i += 1
                    next = col_list[i+1]
                    col_list[k] = (prev + next) / 2
    return cols

'''
找到一列数据中的最大值
返回cols字典
'''
def max_column_data(cols, date_col):
    for col_name in cols:
        if col_name == date_col:
            continue
        max = None
        l = cols[col_name]['list']
        for i,n in enumerate(l):
            if isnum(n):
                n = float(n)
                l[i] = n
                if max is None:
                    max = abs(n)
                elif abs(n) > max:
                    max = abs(n)
        cols[col_name]['max'] = max
    # print(max)
    return cols

'''
将数据根据最大值进行归一化
'''
def standardize_col_data(cols, date_col):
    for col_name in cols:
        if col_name == date_col:
            continue
        standard_list = []
        max = cols[col_name]['max']
        if max == 0:
            standard_list = cols[col_name]['list']
        else:
            for n in cols[col_name]['list']:
                standard_n = n / max
                standard_list.append(standard_n)
        cols[col_name]['standard_list'] = standard_list
    return cols

'''
截取standardize_list到所需的时间范围
截取点间隔可选取为15m或1h
保存为新的standardize_list
'''
def select_data_period(cols, date_col, date, time_interval):
    if date_col in cols.keys():
        td = datetime.datetime.strptime(date, '%m-%d')
        start = 0
        end = 0
        list_end = len(cols[date_col]['list'])
        npts = 0
        step = int(str_to_time(time_interval) / 900)
        for i,d in enumerate(cols[date_col]['list']):
            fd = str_to_datetime(d)
            if time_interval == '1h':
                if td.month != fd.month or td.day != fd.day:
                    start += 1
                elif fd.minute != 0:
                    if not end:
                        start += 1
                else:
                    end = start + 96
                    break
            elif time_interval == '15m':
                if td.month != fd.month or td.day != fd.day:
                    if not end:
                        start += 1
                else:
                    end = start + 96
                    break
        # 完成与时间相关的处理，删除时间列
        npts = len(cols[date_col]['list'][start:end:step])
        cols.pop(date_col)
        for col_name in cols:
            cols[col_name]['standard_list'] = cols[col_name]['standard_list'][start:end:step]
            cols[col_name]['npts'] = npts
        return cols

'''
将col的standard_list输出到指定路径
'''
def cols_to_csv(cols, path, filename):
    for col_name in cols:
        if cols[col_name]['standard_list']:
            if "有功" in col_name:
                file_path = os.path.join(path, filename+"_"+"有功.csv")
                write_log(file_path, cols[col_name]['npts'], 'W', cols[col_name]['max'])
            elif "无功" in col_name:
                file_path = os.path.join(path, filename+"_"+"无功.csv")
                write_log(file_path, cols[col_name]['npts'], 'var', cols[col_name]['max'])
            print("正在输出%s" % file_path)
            f = open(file_path, 'w', newline='')
            writer = csv.writer(f, dialect='excel')
            for i in cols[col_name]['standard_list']:
                writer.writerow([i])
            f.close()

def costomize_settings(settings):
    config_flag = input('是否进行选项设置?(y/n)')
    if config_flag in ['n', 'N']:
        return
    elif config_flag in ['y', 'Y']:
        print('开始设置，请确认用英文输入法输入')
        os.system('pause')
        print('\n设置程序要处理的项目文件夹名\n若程序文件已经在项目文件夹中，则无需填写:\n')
        project_path = input('请输入:')
        print('设置存放负荷数据的文件夹\n')
        data_path = input('请输入:')
        print('设置要进行处理的表名\n'
              + '若不填写，则默认处理第一张表\n'
              + '表名之间用空格分隔\n'
              + '!!!不建议同时处理多张表\n'
              + '!!!如非特殊情况不建议设置\n')
        sheets = input('请输入:')
        sheets = sheets.split(' ')
        print('设置要进行处理的数据表索引(从0开始)'
              + '!!!如非特殊情况不建议设置\n')
        sheets_index = input('请输入:')
        sheets_index = sheets_index.split(' ')
        print('设置需要提取的列名\n'
              + '不同列名之间用空格分隔\n'
              + '!!!请保证输入名称与列名完全一致\n'
              + '!!!若要进行时间处理，请不要将时间列填入此处\n')
        col_names = input('请输入:')
        col_names = col_names.split(' ')
        print('日期序列的列名\n'
              + '若不填写则输出一列中所有数\n')
        date_col = input('请输入:')
        print('设置生成负荷曲线的日期')
        date = input('请输入:')
        print('生成负荷曲线的数据点间隔\n'
              + '目前支持的值为为15m,1h\n'
              + '输入其他间隔可能会有无法按预期工作\n')
        time_interval = input('请输入:')
        if project_path:
            settings['project_path'] = project_path
        if data_path:
            settings['data_path'] = data_path
        if sheets:
            settings['sheets'] = sheets
        if sheets_index:
            settings['sheets_index'] = sheets_index
        if col_names:
            settings['col_names'] = col_names
        if date_col:
            settings['date_col'] = date_col
        if date:
            settings['date'] = date
        if time_interval:
            settings['time_interval'] = time_interval
        return settings
