import pandas as pd

def merge_dataframe(csv_list: list):

  """
  This function takes a csv file list and merge them into a single,
  all csv file should be at the same directory

  """
  if type(csv_list) != list:
    raise Exception('Input should be a list with csv filname')
  dataframes = []
  for csv in csv_list:
    dataframes.append(pd.read_csv(csv))

  dataframe = pd.concat(dataframes, axis = 0)
  return dataframe