#openDSS daily Loadshape generator

This is a simple program for generating Loadshape curve for openDSS Modeling.
The loadshape curve will be output as csv files

##usage

copy the three python files to your project(actually, place the files at any path is fine)

edit `settings.py`

- `project_path`: path to your project. If the python files are placed in the project, then left skip it.
- `data_path`: the name of repository you place your source data files
- `sheets`: If the source data files has more than one sheet, enter the list of names of sheets your want to process
- `sheets_index`: same as above, but in the form of index.
- `col_names`: enter the list of column names you want to process
- `date_col`: if you want to select the data of a certain day, please enter the column name of date
- `date`: enter the date of data you want to process
- `time_interval`: choose the time interval between two points

then run `main.py`
the result file will be generated at the same path as its source file.
meanwhile a file named `data.log` will be generated at the root path of the project to provide you with some additional information

##caveats

 This program now can only process data stored in `.xls` file.
 This program assumes the minimum time interval is 15 minutes, and now it only support switching between 15-minutes and 1-hour.
 If more than one sheets in a single `.xls` file are proecessed by this program, the result of last sheet will override all previous ones.

##TODO

- csv source data file supported
- yearly loadshape generator
- better solution for fixing missing/wrong data
- auto generate `.dss` file
- multi-sheets support
- GUI?

----

This project will probably not be updated anymore since it already satify my own request.

If there are any interesting features that can be added to this program to make openDSS modeling easier,

I'm still willing to do some further development.

So please be free to post **issue** and **pull request**
