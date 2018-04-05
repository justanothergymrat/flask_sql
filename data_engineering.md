

```python
!rm hawaii.sqlite clean_stations.csv clean_measurements.csv
```


```python
import pandas as pd
import numpy as np
import os
```

Use Pandas to read in the measurement and station CSV files as DataFrames.

Inspect the data for NaNs and missing values. You must decide what to do with this data.

Save your cleaned CSV files with the prefix clean_


```python
# process CSVs
measurements_file = "hawaii_measurements.csv"
stations_file = "hawaii_stations.csv"

df_measurements = pd.read_csv(measurements_file)
df_measurements_clean = None

column_list = df_measurements.columns
print('Cleaning ' + measurements_file + "... \n")
for y in range(0,len(column_list)):
    column_name = (column_list[y])
    blank_count = df_measurements[column_name].isnull().sum()
    print("name: " + column_list[y] + ", blanks present: " + str(blank_count))
    if df_measurements[column_name].isnull().sum():
        print('\n NaN or blank cells present in %s, purging those rows \n' % (column_list[y]))
        df_measurements_clean = df_measurements.dropna(axis=0)
        break
    elif y == (len(column_list)-1) and df_measurements_clean is None:
        print('No NaN or blank cells present, creating clean DF \n')
        df_measurements_clean = df_measurements
#         df_measurements_clean = df_measurements.fillna(0)

print("--- \n")

clean_measurements_csv = 'clean_measurements.csv'
df_measurements_clean.to_csv(clean_measurements_csv, index=False)

df_stations = pd.read_csv(stations_file)
df_stations_clean = None

column_list = df_stations.columns
print('Cleaning: ' + stations_file + "... \n")
for y in range(0,len(column_list)):
    column_name = (column_list[y])
    blank_count = df_stations[column_name].isnull().sum()
    print("name: " + column_list[y] + ", blanks present: " + str(blank_count))
    if df_stations[column_name].isnull().sum():
        print('\n NaN or blank cells present in %s, purging those rows \n' % (column_list[y]))
        df_stations_clean = df_stations.dropna(axis=0)
    elif y == (len(column_list)-1) and df_stations_clean is None:
        print('\n No NaN or blank cells present, creating clean DF \n')
        df_stations_clean = df_stations
#         df_stations_clean = df_stations.fillna(0)

clean_stations_csv = 'clean_stations.csv'
df_stations_clean.to_csv(clean_stations_csv, index=False)


```


```python


```
