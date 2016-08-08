settings={
  'project_path':'', #项目地址
  'data_path': 'data', #项目目录下的数据文件夹名
  'sheets': [], #若xls有多张表，则输入需要处理的表名（若处理同一表格的多个表可能会有列重名bug）
  'sheets_index': [], #同sheets作用相同，只是输入待处理表的序号，从0开始
  'col_names': ["瞬时有功(kW)", "←无功(kvar)"], #待处理表中需要归一化的列名
  'date_col': '日期', #若需要截取时间，则输入时间列的列名
  'date': '5-01', # 选取要截取的日期
  'time_interval': '1h' # 最终输出点的时间间隔
}
