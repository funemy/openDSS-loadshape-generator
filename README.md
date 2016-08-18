#openDSS daily Loadshape generator

This is a simple program for generating Loadshape curve for openDSS Modeling.
The loadshape curve will be output as csv files

##usage

copy the three python files to your project(actually, place the files at any path is fine)

edit `settings.py`

- `project_path`: path to your project. If the python files are placed within the project, then skip it.
- `data_path`: the name of repository you place your source data files
- `sheets`: If the source data files has more than one sheet, enter the list of names of sheets your want to process
- `sheets_index`: same as above, but in the form of index.
- `col_names`: enter the list of column names you want to process
- `date_col`: if you want to select the data of a certain day, please enter the column name of date
- `date_col_index`: this option is prior to `date_col`, since the names of date column are not always the same, but in most cases they are placed at first.
- `date`: enter the date of data you want to process
- `time_interval`: choose the time interval between two points

then run `main.py`
the result file will be generated at the same path as its source file.
meanwhile a file named `data.log` will be generated at the root path of the project to provide you with some additional information

##caveats

- this program now can only help you generating daily loadshape curve, so the time interval can only be `5m`/`15m`/`1h` since these are the most common time interval for sampling

- please don't save more than 1 sheets in the `xls` files. The program can still running for now, but the latter one will override the curve of the former. This may never be supported.

- feel free to add column names in the setting even if some of the sheets don't have the column of that name.(since different sheets may have column names. Personally I hate that)

- now the program will process any `csv` and `xls` files including the curve generated last time. This may throw an error. So make sure there are only original data files in the repository every time you run the program.

- the program will auto complement the missing data in the middle, so when choose a date from a period, it is better to choose a date in the middle, or the curve will not be complete.

##TODO

- <del>a better solution to determine the time delta of the original data<del>
- <del>csv source data file supported</del>
- yearly loadshape generator
- better solution for fixing missing/wrong data
- auto generate `.dss` file
- multi-sheets support

##change logs

- v0.0.2 (2016-8-16):
  - add csv file support
  - add one more time interval choice '5m'
  - the implementation of `fix_time_interval` is now more scientific
  - there are more setting options
  - now the program only complement the missing data in the middle, so it's better to choose a date in the middle in case the original data is not complete
  - this version will process any 'csv' and 'xls' including curve generated last time. This will be soon fixed.

- v0.0.3 (2016-8-18)
  - using `pyinstaller` to pack the program into a `exe` file.
  - change the way of reading settings
  - next I will release v1.0.0, following bugs will be fixed:
    - will not reprocess the result file generated last time, so you don't need to delete all old result file for a new run.
    - yearly loadshape of 1h time interval will support(I think it's already supported but I need to do more test)

----
If there are any interesting features that can be added to this program to make openDSS modeling easier,

I'm still willing to do some further development.

So please be free to post **issue** and **pull request**
