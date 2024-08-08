import pandas as pd

def import_inputBREaDS(filename):
    df = pd.read_excel(io = filename,
                       sheet_name = "inputBREaDS")
    df['Datetime'] = pd.to_datetime(df[['Year', 
                                        'Month', 
                                        'Day', 
                                        'Hour']])
    df = df.drop(['Year',
                  'Month',
                  'Day',
                  'Hour'],
                  axis = 1)
    df = df.set_index(['Datetime'])
    return df