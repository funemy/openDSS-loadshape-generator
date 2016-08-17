settings={
  'project_path':'', #项目地址
  'data_path': 'data', #项目目录下的数据文件夹名
  'sheets': [], #若xls有多张表，则输入需要处理的表名（若处理同一表格的多个表可能会有列重名bug）
  'sheets_index': [], #同sheets作用相同，只是输入待处理表的序号，从0开始
  'col_names': ["瞬时有功(kW)", "←无功(kvar)", "值"], #待处理表中需要归一化的列名，请直接复制，包括空格，否则可能获取不到
  'date_col': '', #若需要截取时间，则输入时间列的列名
  'date_col_index': 0, #若不同表的时间列名不同，则可输入时间列的序号，从0开始，优先级更高
  'date': '5-01', # 选取要截取的日期
  'time_interval': '15m' # 最终输出点的时间间隔
}
